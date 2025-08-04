from typing import Annotated
import xgboost as xgb
import mlflow
from mlflow import MlflowClient
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error
import pandas as pd
from utils.tracker_helper import get_tracker_name
from utils.promotion_helper import promote_candidate_in_model_registry, reject_candidate_in_model_registry, CANDIDATE_MODEL, CHAMPION_MODEL
from zenml.client import Client
from zenml.steps import step
from zenml.logger import get_logger


from zenml.client import Client


logger = get_logger(__name__)

@step(
    enable_cache=False
)
def promote_models(
    model_name: str = "xgb-citibike-reg-model",
) -> Annotated[bool, "is_promoted"]:
    logger.info(f"Prompte model")

    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()

    # Retrieve candidate model
    candidate_info = client.get_model_version_by_alias(
        name=model_name, 
        alias=CANDIDATE_MODEL
    )
    logger.info(f"{CANDIDATE_MODEL} model: {candidate_info} {type(candidate_info.version)}")

    is_promoted = False
    # Retrieve champion model
    try:
        champion_info = client.get_model_version_by_alias(
            name=model_name, 
            alias=CHAMPION_MODEL
        )
        logger.info(f"{CHAMPION_MODEL} model: {champion_info} {type(champion_info.version)}")

        # Load models
        '''
        champion_model = mlflow.pyfunc.load_model(f"models:/{registered_model_name}/{champion_info.version}")
        candidate_model = mlflow.pyfunc.load_model(f"models:/{registered_model_name}/{candidate_info.version}")

        # Divide 
        # Evaluar con el conjunto de datos de prueba
        X_test = datasets.drop(columns=[target])
        y_test = datasets[target]

        champion_preds = champion_model.predict(X_test)
        candidate_preds = candidate_model.predict(X_test)
        
        production_rmse = mean_squared_error(y_test, champion_preds)
        candidate_rmse = mean_squared_error(y_test, candidate_preds)
        '''
        candidate_rmse = float(candidate_info.tags["rmse"])
        production_rmse = float(champion_info.tags["rmse"])

        logger.info(f"RMSE staging model   : {candidate_rmse}")
        logger.info(f"RMSE production model: {production_rmse}")

        # Promover el modelo candidato si es mejor
        if candidate_rmse < production_rmse:
            # Candidate is better; archive current production.
            promote_candidate_in_model_registry(
                model_name=model_name,
                latest_version=candidate_info.version,
                current_version=champion_info.version,
            )
            logger.info(f"Candidate promoted to Production. Candidate model ({candidate_info.version}) has lower MAE ({candidate_rmse}) than current production ({production_rmse}).")
            is_promoted = True
        else:
            # Production is better, archive staging
            # Candidate is not better; leave it archived.
            reject_candidate_in_model_registry(
                model_name=model_name,
                current_version=candidate_info.version
            )
            logger.info("Candidate is not better; leave it archived.")

    except Exception as e:
        logger.info(f"Error fetching  previous production model: {str(e)}")
        # No production model exists, so mark the candidate as Production.
        promote_candidate_in_model_registry(
            model_name=model_name,
            latest_version=candidate_info.version,
            current_version=None,
        )
        logger.info(f"Completed: Auto Promotion of Staging to Production")
        is_promoted = True

    return is_promoted


    
@step(
    enable_cache=False
)
def get_model_by_alias(
    model_name: str,
    model_alias: str
#) -> Tuple[Annotated[xgb.XGBRegressor, "registered_model"], Annotated[ModelVersion, "model_version"]]:
) -> Annotated[xgb.XGBRegressor, "registered_model"]:
    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()

    logger.info(f"Retrieve info model {model_name} with alias {model_alias}")
    model_version = client.get_model_version_by_alias(
        name=model_name, 
        alias=model_alias
    )
    logger.info(f"Model version: {model_version}")

    # Load model
    model_uri = model_version.source
    model = mlflow.xgboost.load_model(model_uri=model_uri)
    logger.info(f"Retrieve info model {model_name} with alias {model_alias}, model: {type(model)}")
    return model    

