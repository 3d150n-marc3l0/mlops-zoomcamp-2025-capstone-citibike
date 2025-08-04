from typing_extensions import Tuple, Annotated, List
import xgboost as xgb
import pandas as pd
from zenml import step
from zenml.integrations.mlflow.services.mlflow_deployment import (
    MLFlowDeploymentService,
)
from zenml.logger import get_logger

from steps.data_loaders import DATASET_PREDICTION_COLUMN_NAME

logger = get_logger(__name__)


@step
def inference_predict(
    model: xgb.XGBRegressor,
    dataset_inf: pd.DataFrame,
    categorical_feats: List[str] = [],
	numerical_feats: List[str] = []
) -> Tuple[
    Annotated[pd.DataFrame, "predictions"],
    Annotated[str, "prediction"]
]:
    """Predictions step.

    This is an example of a predictions step that takes the data in and returns
    predicted values.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured to use different input data.
    See the documentation for more information:

        https://docs.zenml.io/how-to/build-pipelines/use-pipeline-step-parameters

    Args:
        dataset_inf: The inference dataset.

    Returns:
        The predictions as pandas series
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###

    X = dataset_inf[categorical_feats + numerical_feats]
   
    dataset_inf[DATASET_PREDICTION_COLUMN_NAME] = model.predict(X)

    ### YOUR CODE ENDS HERE ###

    return dataset_inf, DATASET_PREDICTION_COLUMN_NAME