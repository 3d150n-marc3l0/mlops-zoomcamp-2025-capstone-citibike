import mlflow
from mlflow.tracking import MlflowClient
from sklearn.metrics import mean_squared_error
import numpy as np
from zenml import step
from zenml.integrations.evidently.metrics import EvidentlyMetricConfig
from zenml.integrations.evidently.steps import (
    EvidentlyColumnMapping,
    evidently_report_step, 
    evidently_test_step,
)
from zenml.integrations.evidently.tests import EvidentlyTestConfig

from steps.data_loaders import (
    DATASET_TARGET_COLUMN_NAME, 
    DATASET_NUMERICAL_COLUMNS, 
    DATASET_CATEGORICAL_COLUMNS,
    DATASET_PREDICTION_COLUMN_NAME
)


# Detector data drift
citibike_data_drift_report = evidently_report_step.with_options(
    parameters=dict(
        column_mapping=EvidentlyColumnMapping(
            target=DATASET_TARGET_COLUMN_NAME,
            numerical_features=DATASET_NUMERICAL_COLUMNS,
            categorical_features=DATASET_CATEGORICAL_COLUMNS,
            prediction=DATASET_PREDICTION_COLUMN_NAME
        ),
        metrics=[
            EvidentlyMetricConfig.metric("ColumnDriftMetric", column_name='prediction'),
            EvidentlyMetricConfig.metric("DatasetDriftMetric"),
            EvidentlyMetricConfig.metric("DatasetMissingValuesMetric"),
            EvidentlyMetricConfig.metric("DatasetDriftMetric"),
            EvidentlyMetricConfig.metric("RegressionPreset")
        ]
    )
)

citibike_data_drift_test = evidently_test_step.with_options(
    parameters=dict(
        column_mapping=EvidentlyColumnMapping(
            target=DATASET_TARGET_COLUMN_NAME,
            numerical_features=DATASET_NUMERICAL_COLUMNS,
            categorical_features=DATASET_CATEGORICAL_COLUMNS,
            prediction=DATASET_PREDICTION_COLUMN_NAME
        ),
        tests=[
            EvidentlyTestConfig.test("DataQualityTestPreset"),
        ],
        # We need to download the NLTK data for the TestColumnRegExp test
        #download_nltk_data=True,
    ),
)