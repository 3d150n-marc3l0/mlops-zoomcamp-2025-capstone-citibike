from typing import Annotated, Dict
import yaml
import click
from pipelines.training import citibike_training_pipeline
from pipelines.deployment import (
    bentoml_deployment_pipeline,
    local_citibike_deployment_pipeline,
)
from pipelines.monitoring import batch_monitoring_backfill
from zenml.logger import get_logger

logger = get_logger(__name__)


def read_config(config_path: str) -> Annotated[Dict, "config"]:
    logger.info(f"Reading file: {config_path}")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


TRAINING_PIPELINE_NAME = "training"
MLFLOW_DEPLOYMENT_PIPELINE_NAME = "deploy-mlflow"
BENTOML_DEPLOYMENT_PIPELINE_NAME = "deploy-bentoml"
MONITORING_DEPLOYMENT_PIPELINE_NAME = "monitoring"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-p",
    "--pipeline",
    type=str,
    required=True,
    help="Pipeline name",
)
@click.option(
    "-c",
    "--config_path",
    type=str,
    required=True,
    help="Config file",
    metavar="<FILE>",
)
def main(
    pipeline: str,
    config_path: str,
):
    logger.info("Init command")

    print(f"pipeline: {pipeline}")
    print(f"tconfig_pathst_size: {config_path}")

    base_config = read_config(config_path)
    assert "pipelines" in base_config, "Don't found 'pipelines' key"
    pipelines_config = base_config["pipelines"]

    if pipeline == TRAINING_PIPELINE_NAME:
        logger.info(f"Runing {pipeline} ...")
        assert "parameters" in pipelines_config.get(
            pipeline, {}
        ), f"Don't found '{pipeline}' config"
        train_config = pipelines_config[pipeline]["parameters"]
        print(train_config)
        # citibike_training_pipeline(**train_config)
        citibike_training_pipeline(
            data_url=train_config["data_url"],
            start_train_date=train_config["start_train_date"],
            end_train_date=train_config["end_train_date"],
            test_size=train_config["test_size"],
            shuffle=train_config["shuffle"],
            random_state=train_config["random_state"],
            n_trials=train_config["n_trials"],
            registered_model_name=train_config["registered_model_name"],
        )

    elif pipeline == MLFLOW_DEPLOYMENT_PIPELINE_NAME:
        logger.info(f"Runing {pipeline} ...")
        assert "parameters" in pipelines_config.get(
            pipeline, {}
        ), f"Don't found '{pipeline}' config"
        deploy_config = pipelines_config[pipeline]["parameters"]
        logger.info(deploy_config)
        local_citibike_deployment_pipeline(**deploy_config)

    elif pipeline == BENTOML_DEPLOYMENT_PIPELINE_NAME:
        logger.info(f"Runing {pipeline} ...")
        assert "parameters" in pipelines_config.get(
            pipeline, {}
        ), f"Don't found '{pipeline}' config"
        deploy_config = pipelines_config[pipeline]["parameters"]
        logger.info(deploy_config)
        bentoml_deployment_pipeline(**deploy_config)

    elif pipeline == MONITORING_DEPLOYMENT_PIPELINE_NAME:
        logger.info(f"Runing {pipeline} ...")
        assert "parameters" in pipelines_config.get(
            pipeline, {}
        ), f"Don't found '{pipeline}' config"
        monitor_config = pipelines_config[pipeline]["parameters"]
        logger.info(monitor_config)
        batch_monitoring_backfill(**monitor_config)
    else:
        raise f"Don't recognize command {pipeline}"


if __name__ == "__main__":

    main()
