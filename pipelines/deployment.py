from typing import List
import zenml
from zenml import pipeline
from zenml.integrations.bentoml.steps import (
    bento_builder_step,
    bentoml_model_deployer_step,
)
from zenml.integrations.bentoml.services import BentoMLDeploymentType
from zenml.logger import get_logger
from steps import (
    local_mlflow_deployment_deploy,
    get_model_by_alias,
    notify_on_success,
)

logger = get_logger(__name__)


@pipeline
def local_citibike_deployment_pipeline(model_name: str, model_alias: str):
    """
    Model deployment pipeline.

    This is a pipeline deploys trained model for future inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    ########## Deployment stage ##########
    local_mlflow_deployment_deploy(
        model_name=model_name, model_alias=model_alias
    )

    # notify_on_success(after=["local_deployment_deploy"])
    ### YOUR CODE ENDS HERE ###


@pipeline
def bentoml_deployment_pipeline(
    model_name: str,
    model_alias: str,
    service_class: str,
    working_dir: str,
    image_name: str,
    image_tag: str,
    packages: List[str],
):

    logger.info("Star deploy wth bentoml")

    model = get_model_by_alias(model_name=model_name, model_alias=model_alias)
    logger.info(f"Star deploy wth bentoml {type(model)}")

    # "service.py:CitibikeService"
    # Build the BentoML bundle
    bento = bento_builder_step(
        model=model,
        model_name=model_name,  # tu nuevo nombre de modelo para Bento
        model_type="xgboost",  # puede ser 'sklearn' o 'xgboost'
        service=service_class,  # tu clase de servicio en BentoML
        labels={
            "framework": "xgboost",
            "dataset": "citibike",
            "zenml_version": f"{zenml.__version__}",
        },
        exclude=["data"],
        python={"packages": packages},
        working_dir=working_dir,  # "./service"
    )

    # image_tag = f"v{model_version.version}"
    deployed_model = bentoml_model_deployer_step(
        bento=bento,
        model_name=model_name,  # Name of the model
        port=3000,  # Port to be used by the http server
        deployment_type=BentoMLDeploymentType.CONTAINER,
        image=image_name,
        # image_tag=image_tag,
        platform="linux/amd64",
    )

    return deployed_model
