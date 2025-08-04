from typing import Tuple, Annotated, List
import xgboost as xgb
import bentoml
import os
import mlflow
from mlflow.entities.model_registry import ModelVersion
from bentoml import bentos
from bentoml.types import ModelSignature
from mlflow.tracking import MlflowClient, artifact_utils
import zenml
from zenml import pipeline, step #, get_step_context
from zenml.client import Client
from zenml.integrations.mlflow.steps import (
    mlflow_deployer,

)
from zenml.integrations.bentoml.steps import (
    bento_builder_step,
    bentoml_model_deployer_step 
)
from zenml.integrations.bentoml.services import BentoMLDeploymentType
from zenml.logger import get_logger
from steps import (
    local_mlflow_deployment_deploy,
    get_model_by_alias,
    notify_on_success
)

logger = get_logger(__name__)

@pipeline
def local_citibike_deployment_pipeline(
    model_name: str,
    model_alias: str
):
    """
    Model deployment pipeline.

    This is a pipeline deploys trained model for future inference.
    """

    '''
    # Retrieve candidate model
    model = ''

    # Build
    bento = bento_builder_step(
        model=model,
        model_name="pytorch_mnist",  # Name of the model
        model_type="xgboost",  # Type of the model (pytorch, tensorflow, sklearn, xgboost..)
        service="service.py:CitiBikeService",  # Path to the service file within zenml repo
        labels={  # Labels to be added to the bento bundle
            "framework": "pytorch",
            "dataset": "mnist",
            "zenml_version": "0.21.1",
        },
        exclude=["data"],  # Exclude files from the bento bundle
        python={
            "packages": ["zenml", "torch", "torchvision"],
        },  # Python package requirements of the model
    )

    # Deplymente
    deployed_model = bentoml_model_deployer_step(
        bento=bento,
        model_name="pytorch_mnist",  # Name of the model
        port=3001,  # Port to be used by the http server
        deployment_type="container",
        image="my-custom-image",
        image_tag="my-custom-image-tag",
        platform="linux/amd64",
    ) 
    '''

        
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## Deployment stage ##########
    local_mlflow_deployment_deploy(
        model_name=model_name,
        model_alias=model_alias
    )

    

    #notify_on_success(after=["local_deployment_deploy"])
    ### YOUR CODE ENDS HERE ###



'''

@step(
    enable_cache=False
)
def save_bentoml(
    model_name:str,
    working_dir:str
):
    bentoml.models.export_model(f'{model_name}:latest', os.path.join(working_dir, f"{model_name}.bentomodel"))
'''

@pipeline
def bentoml_deployment_pipeline(
    model_name: str,
    model_alias: str,
    service_class: str,
    working_dir: str,
    image_name: str,
    image_tag: str,
    packages: List[str]
):
    
    logger.info("Star deploy wth bentoml")
    #mv = get_step_context().model_version
    #m = get_step_context().model_version
    #logger.info(f"Star deploy wth bentoml {mv}")
    #logger.info(f"Star deploy wth bentoml {m}")
    

    model = get_model_by_alias(
        model_name=model_name, 
        model_alias=model_alias
    )
    logger.info(f"Star deploy wth bentoml {type(model)}")
    


    '''
    cleaned_packages = [
        "zenml==0.83.1",
        "mlflow==2.22.1",
        "numpy==1.26.4",
        "pandas==2.3.1",
        "psutil==5.9.8",
        "scikit-learn==1.7.0",
        "scipy==1.16.0",
        "xgboost==3.0.2",
    ]
    save_bentoml(
        model_name=model_name,
        working_dir=working_dir
    )
    '''

    #"service.py:CitibikeService"
    # Build the BentoML bundle
    bento = bento_builder_step(
        model=model,
        model_name=model_name,  # tu nuevo nombre de modelo para Bento
        model_type="xgboost",        # puede ser 'sklearn' o 'xgboost'
        service=service_class,  # tu clase de servicio en BentoML
        labels={
            "framework": "xgboost",
            "dataset": "citibike",
            "zenml_version": f"{zenml.__version__}",
        },
        exclude=["data"],
        python={
            "packages": packages
        },
        working_dir=working_dir #"./service"
    )

    #image_tag = f"v{model_version.version}"
    deployed_model = bentoml_model_deployer_step(
        bento=bento,
        model_name=model_name,  # Name of the model
        port=3000,  # Port to be used by the http server
        deployment_type=BentoMLDeploymentType.CONTAINER,
        image=image_name,
        #image_tag=image_tag,
        platform="linux/amd64",
    )
    

    '''
    #get_step_context().model

    zenml_client = Client()
    model_registry = zenml_client.active_stack.model_registry
    model_deployer = zenml_client.active_stack.model_deployer
    logger.info(f"model_deployer    : {model_registry}")
    logger.info(f"experiment_tracker: {model_deployer}")
    # Let's get the run id of the current pipeline
    # Once we have the run id, we can get the model URI using mlflow client
    model_registry.configure_mlflow()

    client = MlflowClient()
    champion_model_version = client.get_model_version_by_alias(model_name, model_alias)
    logger.info(f"champion_model_version: {champion_model_version}")
    mlflow_run_id = champion_model_version.run_id
    model_uri = champion_model_version.source
    bento_model = bentoml.mlflow.import_model(
        name=model_name,
        model_uri=model_uri
    )

    logger.info(f"bento_model: {bento_model.info()}")

    # Retrieve candidate model
    model = ''

    # Build
    bento = bento_builder_step(
        model=model,
        model_name="pytorch_mnist",  # Name of the model
        model_type="xgboost",  # Type of the model (pytorch, tensorflow, sklearn, xgboost..)
        service="service.py:CitiBikeService",  # Path to the service file within zenml repo
        labels={  # Labels to be added to the bento bundle
            "framework": "pytorch",
            "dataset": "mnist",
            "zenml_version": "0.21.1",
        },
        exclude=["data"],  # Exclude files from the bento bundle
        python={
            "packages": ["zenml", "torch", "torchvision"],
        },  # Python package requirements of the model
    )

    # Deplyomente
    deployed_model = bentoml_model_deployer_step(
        bento=bento,
        model_name="pytorch_mnist",  # Name of the model
        port=3001,  # Port to be used by the http server
        deployment_type=BentoMLDeploymentType.CONTAINER,
        image="my-custom-image",
        image_tag="my-custom-image-tag",
        platform="linux/amd64",
    )


    #notify_on_success(after=["local_deployment_deploy"])
    ### YOUR CODE ENDS HERE ###
    '''