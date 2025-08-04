from typing import Dict, Optional, Annotated
from zenml.client import Client
from mlflow import MlflowClient
import mlflow
import xgboost as xgb
from zenml.logger import get_logger


logger = get_logger(__name__)

# Alias
CANDIDATE_MODEL = "candidate"
CHAMPION_MODEL = "champion"
#DEPRECATED_MODEL = "deprecated"

# Stage Key
STAGE_KEY = "stage"
STAGING_STAGE = "Staging"
PRODUCTION_STAGE = "Production"
ARCHIVED_STAGE = "Archived"

# Status Key
STATUS_KEY = "validation_status"
APPROVED_STATUS = "approved"
PENDING_STATUS  = "pending"
REJECTED_STATUS = "rejected"

# RMSE Key
METRIC_KEY = "rmse"


def get_model_by_alias(
    model_name: str,
    model_alias: str
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

    return model


def get_model_version_by_alias(
    model_name: str,
    alias: str
):
    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()

    logger.info(f"Retrieve info model {model_name} with alias {alias}")
    model_version = client.get_model_version_by_alias(
        name=model_name, 
        alias=alias
    )
    logger.info(f"Model version: {model_version}")

    return model_version



def register_candidate_in_model_registry(
    model_name: str,
    metrics: Dict
):
    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()
    
    # Alias
    # Use aliases instead of deprecated stages for deployment management
    # Set aliases for different deployment environments
    model_version = client.get_latest_versions(model_name)[0]

    # Register model like candidate
    client.set_registered_model_alias(
        name=model_name,
        alias=CANDIDATE_MODEL,  # A/B testing model
        version=model_version.version,
    )
    # Add Staging Tag 
    metadata = {
        STAGE_KEY: STAGING_STAGE,        # Staging Stage
        STATUS_KEY: PENDING_STATUS,      # Approvaded Status
        **metrics  #METRIC_KEY: str(metrics["rmse"])  # Metrics
    }
    for key, value in metadata.items():
        client.set_model_version_tag(
            name=model_name,
            version=model_version.version,
            key=key,
            value=value
        )



def reject_candidate_in_model_registry(
    model_name: str,
    current_version: str,
):
    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()
    # Staging to Archived
    client.set_model_version_tag(
        name=model_name,
        version=current_version.version,
        key=STAGE_KEY,
        value=ARCHIVED_STAGE
    )



def promote_candidate_in_model_registry(
    model_name: str, 
    latest_version: str, 
    current_version: Optional[str] = None, 
):
    logger.info(f"model_name: {model_name}, latest_version: {latest_version}, current_version: {current_version}")
    model_registry = Client().active_stack.model_registry
    model_registry.configure_mlflow()
    client = MlflowClient()

    # Candidate is better; archive current production.
    if current_version:
        client.set_model_version_tag(
            name=model_name,
            version=current_version,
            key=STAGE_KEY,
            value=ARCHIVED_STAGE
        )
    # Promote the candidate.
    logger.info("Remove candidate alias.")
    client.delete_registered_model_alias(
        name=model_name,
        alias=CANDIDATE_MODEL
    )
    logger.info("Add champion alias.")
    client.set_registered_model_alias(
        name=model_name,
        alias=CHAMPION_MODEL,
        version=latest_version,
    )
    logger.info("Add tags champion.")
    # Add Tags:
    # Stage : Staging to Production
    # Status: Pending to Approved
    metadata = {
        STAGE_KEY: PRODUCTION_STAGE, # Production Stage
        STATUS_KEY: APPROVED_STATUS  # Approvaded Status
    }
    for key, value in metadata.items():
        client.set_model_version_tag(
            name=model_name,
            version=latest_version,
            key=key,
            value=value
        )
    
    logger.info("Success promtion model.")