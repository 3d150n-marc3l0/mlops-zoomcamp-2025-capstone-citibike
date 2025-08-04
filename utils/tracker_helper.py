from typing import Optional
from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers import (
    MLFlowExperimentTracker,
)

LOCAL_MLFLOW_UI_PORT = 8185


def get_tracker_name() -> Optional[str]:
    """Get the name of the active experiment tracker."""

    experiment_tracker = Client().active_stack.experiment_tracker
    return experiment_tracker.name if experiment_tracker else None