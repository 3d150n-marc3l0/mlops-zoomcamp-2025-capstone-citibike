"""Data validation steps used to check the input data quality and to ensure that
the training and validation data have the same distribution."""

from functools import partial


from zenml.integrations.evidently.metrics import EvidentlyMetricConfig
from zenml.integrations.evidently.steps import (
    EvidentlyColumnMapping,
    evidently_report_step, 
    evidently_test_step,
)
from zenml.integrations.evidently.tests import EvidentlyTestConfig

from steps.data_loaders import DATASET_TARGET_COLUMN_NAME, DATASET_NUMERICAL_COLUMNS, DATASET_CATEGORICAL_COLUMNS


# Detector data drift
citibike_data_report = evidently_report_step.with_options(
    parameters=dict(
        column_mapping=EvidentlyColumnMapping(
            target=DATASET_TARGET_COLUMN_NAME,
            numerical_features=DATASET_NUMERICAL_COLUMNS,
            #categorical_features=DATASET_CATEGORICAL_COLUMNS
        ),
        metrics=[
            EvidentlyMetricConfig.metric("DataQualityPreset")
        ]
    )
)

citibike_data_test = evidently_test_step.with_options(
    parameters=dict(
        column_mapping=EvidentlyColumnMapping(
            target=DATASET_TARGET_COLUMN_NAME,
            numerical_features=DATASET_NUMERICAL_COLUMNS,
            #categorical_features=DATASET_CATEGORICAL_COLUMNS
        ),
        tests=[
            EvidentlyTestConfig.test("DataQualityTestPreset"),
        ],
        # We need to download the NLTK data for the TestColumnRegExp test
        #download_nltk_data=True,
    ),
)


