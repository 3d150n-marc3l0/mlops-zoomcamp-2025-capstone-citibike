from typing import Dict, Any
import mlflow
from mlflow import MlflowClient
from mlflow.models.signature import infer_signature
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import xgboost as xgb
from utils.tracker_helper import get_tracker_name
from utils.promotion_helper import register_candidate_in_model_registry
from zenml import step
from zenml.logger import get_logger



@step(
    experiment_tracker=get_tracker_name(), 
    enable_cache=False
)
def register_model(
    model: xgb.XGBRegressor, 
    metrics: Dict,
    dataset: pd.DataFrame,
    target: str,
    model_name: str = "xgb-citibike-reg-model"
) -> None:
    
    logger = get_logger(__name__)
    logger.info("Registering model to MLflow")

    # Divide features y target
    X = dataset.drop(columns=[target])
    y = dataset[target]

    # Inferir la firma del modelo
    signature = infer_signature(X, model.predict(X))

    # Register model
    mlflow.xgboost.log_model(
        xgb_model=model,
        artifact_path="model",
        #name="xgb-citibike",
        registered_model_name=model_name,
        signature=signature,
        input_example=X.iloc[:1],  # ejemplo de una fila, también es un DataFrame
        model_format="json",
    )
    mlflow.log_metrics(metrics=metrics)

    # Register candidate
    register_candidate_in_model_registry(
        model_name=model_name,
        metrics=metrics
    )
    logger.info("Registering model to Success")