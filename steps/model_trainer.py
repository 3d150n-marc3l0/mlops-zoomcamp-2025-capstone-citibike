from typing import Dict, Annotated
from sklearn.base import ClassifierMixin
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import pandas as pd
import xgboost as xgb
import mlflow
from mlflow.models.signature import infer_signature
from utils.tracker_helper import get_tracker_name
from zenml import step


@step(
    experiment_tracker=get_tracker_name(), 
    enable_cache=False
)
def xgb_trainer(
    dataset: pd.DataFrame, 
    target: str, 
    params: Dict
) -> Annotated[xgb.XGBRegressor, "trained_model"]:
    mlflow.autolog()

    # Divide X and y
    X = dataset.drop(columns=[target])
    y = dataset[target]

    # Crea el modelo con hiperparámetros optimizados
    model = xgb.XGBRegressor(**params)
    model.fit(X, y)
     
    # Predicciones para inferir la firma
    y_pred = model.predict(X)
    
    mlflow.log_params(params)
    mlflow.log_metric("train_r2", r2_score(y, y_pred))
    mlflow.log_metric("train_mae", mean_absolute_error(y, y_pred))
    mlflow.log_metric("train_mse", mean_squared_error(y, y_pred))
    mlflow.log_metric("train_rmse", root_mean_squared_error(y, y_pred))

    '''
    # Predicciones para inferir la firma
    y_pred = model.predict(X)
    signature = infer_signature(X, y_pred)

    # Ejemplo de input para inferencia
    input_example = X.sample(1)

    # Logging a MLflow (ZenML maneja el contexto)
    mlflow.log_params(params)
    mlflow.xgboost.log_model(
        xgb_model=model.get_booster(),
        artifact_path="model",
        signature=signature,
        input_example=input_example
    )
    '''

    return model
