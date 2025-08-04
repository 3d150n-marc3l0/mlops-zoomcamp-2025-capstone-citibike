import datetime
from zenml import pipeline
from zenml.logger import get_logger
from steps.data_validator import (
    DATASET_CATEGORICAL_COLUMNS,
    DATASET_NUMERICAL_COLUMNS,
    DATASET_TARGET_COLUMN_NAME,
)
from steps import (
    reference_data_loader,
    get_model_by_alias,
    data_preprocessor,
    citibike_data_drift_report,
    inference_predict,
    calculate_drift_metrics_step,
    create_table_step,
    save_metrics_to_db_step,
)

logger = get_logger(__name__)


@pipeline
def batch_monitoring_backfill(
    data_url: str,
    model_name: str,
    model_alias: str,
    host: str,
    port: int,
    database: str,
    start_reference_date: str,
    end_reference_date: str,
    start_current_date: str,
    end_current_date: str,
):
    logger.info("Starting monitoring")
    logger.info(
        f"data_url: {data_url}, model_name: {model_name}, model_alias: {model_alias}"
    )
    logger.info(
        f"start_reference_date: {start_reference_date}, end_reference_date: {end_reference_date}"
    )
    logger.info(
        f"start_current_date: {start_current_date}, end_current_date: {end_current_date}"
    )
    start_reference_date = datetime.datetime.strptime(
        start_reference_date, "%Y-%m-%d"
    )
    end_reference_date = datetime.datetime.strptime(
        end_reference_date, "%Y-%m-%d"
    )
    start_current_date = datetime.datetime.strptime(
        start_current_date, "%Y-%m-%d"
    )
    end_current_date = datetime.datetime.strptime(end_current_date, "%Y-%m-%d")

    # Read
    create_table_step(host=host, port=port, database=database)

    # Get model
    model = get_model_by_alias(
        model_name=model_name,
        model_alias=model_alias,
        after=["create_table_step"],
    )

    # Retrieve
    reference_data, comparison_data, target_col = reference_data_loader(
        base_url=data_url,
        start_reference_date=start_reference_date,
        end_reference_date=end_reference_date,
        start_current_date=start_current_date,
        end_current_date=end_current_date,
        after=["get_model_by_alias"],
    )

    # Clean
    reference_data = data_preprocessor(reference_data, is_reference=True)
    comparison_data = data_preprocessor(comparison_data, is_reference=True)

    # Inference
    reference_data, _ = inference_predict(
        model=model,
        dataset_inf=reference_data,
        categorical_feats=DATASET_CATEGORICAL_COLUMNS,
        numerical_feats=DATASET_NUMERICAL_COLUMNS,
    )
    comparison_data, prediction_col = inference_predict(
        model=model,
        dataset_inf=comparison_data,
        categorical_feats=DATASET_CATEGORICAL_COLUMNS,
        numerical_feats=DATASET_NUMERICAL_COLUMNS,
    )

    json_report, html_report = citibike_data_drift_report(
        reference_dataset=reference_data,
        comparison_dataset=comparison_data,
    )

    # Range
    metrics = calculate_drift_metrics_step(
        reference_data=reference_data,
        current_data=comparison_data,
        target=target_col,
        prediction=prediction_col,
        categorical_feats=DATASET_CATEGORICAL_COLUMNS,
        numerical_feats=DATASET_NUMERICAL_COLUMNS,
    )

    save_metrics_to_db_step(
        host=host, port=port, database=database, metrics=metrics
    )

    logger.info("End monitoring")
