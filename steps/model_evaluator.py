import logging
from typing import Any, Dict, Annotated
from typing import Tuple
from typing_extensions import Annotated
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    mean_squared_error, 
    root_mean_squared_error, 
    r2_score
)
import mlflow
from zenml import step
from steps.data_loaders import DATASET_TARGET_COLUMN_NAME


from utils.tracker_helper import get_tracker_name

@step(
    experiment_tracker=get_tracker_name()
)
def model_scorer(
    model: Any,
    dataset: pd.DataFrame,
    target: str
#) -> Tuple[Annotated[float, "r2"], Annotated[float, "mse"], Annotated[float, "rmse"]]:
) -> Annotated[Dict, "metrics"]:
    try:
        # Divide X and y
        X = dataset.drop(columns=[target])
        y = dataset[target]

        # Make predictions using the model
        y_pred = model.predict(X)

        # Using the MSE class for mean squared error calculation
        mse = mean_squared_error(y, y_pred)
        mlflow.log_metric("mse", mse)

        # Using the R2Score class for R2 score calculation
        r2 = r2_score(y, y_pred)
        mlflow.log_metric("r2", r2)

        # Using the RMSE class for root mean squared error calculation
        rmse = root_mean_squared_error(y, y_pred)
        mlflow.log_metric("rmse", rmse)

        return {
            "r2": r2, 
            "mse": mse, 
            "rmse": rmse
        }
    except Exception as e:
        logging.error("error in evaluation".format(e))
        raise e