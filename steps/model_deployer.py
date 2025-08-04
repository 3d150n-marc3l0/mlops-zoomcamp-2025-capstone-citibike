from typing import Optional
from zenml import pipeline, step, get_step_context
from zenml.client import Client
from mlflow.tracking import MlflowClient, artifact_utils
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from zenml.integrations.mlflow.services import MLFlowDeploymentConfig
from zenml.logger import get_logger
from steps.model_promoter import CHAMPION_MODEL


logger = get_logger(__name__)

@step(
    enable_cache=False
)
def local_mlflow_deployment_deploy(
    model_name: str,
    model_alias: str
) -> Optional[MLFlowDeploymentService]:
    
    logger.info(f"Deploy local model")

    # Deploy a model using the MLflow Model Deployer
    zenml_client = Client()
    model_deployer = zenml_client.active_stack.model_deployer
    experiment_tracker = zenml_client.active_stack.experiment_tracker
    logger.info(f"model_deployer    : {model_deployer}")
    logger.info(f"experiment_tracker: {model_deployer}")
    # Let's get the run id of the current pipeline
    
    '''
    mlflow_run_id = experiment_tracker.get_run_id(
        experiment_name=get_step_context().pipeline_name,
        run_name=get_step_context().run_name,
    )
    '''
    # Once we have the run id, we can get the model URI using mlflow client
    experiment_tracker.configure_mlflow()
    
    
    client = MlflowClient()
    champion_model_version = client.get_model_version_by_alias(model_name, model_alias)
    logger.info(f"champion_model_version: {champion_model_version}")
    mlflow_run_id = champion_model_version.run_id
    #model_name = champion_model_version.name  # set the model name that was logged
    logger.info(f"run_id: {mlflow_run_id} model_name: {model_name}")
    artifact_path="model"
    model_uri = artifact_utils.get_artifact_uri(
        run_id=mlflow_run_id, artifact_path=artifact_path
    )
    mlflow_deployment_config = MLFlowDeploymentConfig(
        model_uri=model_uri,
        model_name=model_name,
        workers = 1,
        mlserver = False,
        timeout = 300,
    )
    service = model_deployer.deploy_model(
        config=mlflow_deployment_config, 
        service_type=MLFlowDeploymentService.SERVICE_TYPE,
        replace=True
    )
    return service