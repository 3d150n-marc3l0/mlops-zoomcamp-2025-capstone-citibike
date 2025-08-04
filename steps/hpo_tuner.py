from typing import Dict, Annotated
import optuna
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
import xgboost as xgb
from zenml import step
import numpy as np

@step(
    enable_cache=False
)
def optimize_hyperparams(
    dataset: pd.DataFrame, 
    target: str, 
    n_trials: int = 50
) -> Annotated[Dict, "best_params"]:
    def objective(trial):
        # Espacio de búsqueda de hiperparámetros
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 0, 1.0),
            "reg_lambda": trial.suggest_float("reg_lambda", 0, 1.0),
            "objective": "reg:squarederror",  # Para regresión
            "random_state": 42,
            "n_jobs": -1
        }

        model = xgb.XGBRegressor(**params)

        # Validación cruzada con RMSE negativo (porque scikit-learn lo invierte)
        cv = KFold(n_splits=3, shuffle=True, random_state=42)
        scores = cross_val_score(model, X, y, scoring="neg_root_mean_squared_error", cv=cv)
        return np.mean(scores)  # mayor = mejor
    
    # Divide X and y
    X = dataset.drop(columns=[target])
    y = dataset[target]

    # Maximiza el valor negativo del RMSE (menor RMSE)
    study = optuna.create_study(
        direction="maximize" # Direction of optimization. Set minimize for minimization and maximize for maximization.
    )
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_params["objective"] = "reg:squarederror"  # asegurar que se mantenga

    return best_params
