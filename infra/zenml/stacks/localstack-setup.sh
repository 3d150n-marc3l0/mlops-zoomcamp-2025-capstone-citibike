#!/bin/sh
echo "Setup: Initializing localstack s3"

ENDPOINT=http://localhost:4566  # LOCALSTACK
#ENDPOINT=http://localhost:9000  # MINIO

# Infra zenml
ZENML_INFRA_DIR=$PWD/infra/zenml

# Experiment directory
EXPERIMENT_DIR=$PWD/experiments
ZENML_EXPERIMENT_DIR=$EXPERIMENT_DIR/zenml
MLFLOW_EXPERIMENT_DIR=$EXPERIMENT_DIR/mflow

# Data Directory
CITIBIKE_DATA_DIR=$PWD/data 
RAW_DATA_DIR=$CITIBIKE_DATA_DIR/raw
PROCESSED_DATA_DIR=$CITIBIKE_DATA_DIR/processed

# Buckets S3 in localstack
ZENML_BUCKET=zenml-artifacts            # zenml bucket
MLFLOW_BUCKET=mlflow-artifacts          # mlflow bucket
CITIBIKE_DATASET_BUCKET=citibike-data   # citibike datasets bucket

echo "Experiment directorory: ${EXPERIMENT_DIR}"

###################### ZenML: Artifact Store ######################
# Create bucket
aws --endpoint-url=$ENDPOINT s3 mb s3://$ZENML_BUCKET

# Restore backup zenml
echo "Restore zenml experiment directory: ${ZENML_EXPERIMENT_DIR}"
[ -d "${ZENML_EXPERIMENT_DIR}" ] && echo "Directory ${ZENML_EXPERIMENT_DIR} exists." && aws --endpoint-url=$ENDPOINT s3 cp $ZENML_EXPERIMENT_DIR s3://$ZENML_BUCKET/ --recursive

###################### Mlfow ######################
aws --endpoint-url=$ENDPOINT s3 mb s3://$MLFLOW_BUCKET

# Restore backup mlflow
echo "Restore mlflow experiment directory: ${MLFLOW_EXPERIMENT_DIR}"
[ -d "${MLFLOW_EXPERIMENT_DIR}" ] && echo "Directory ${MLFLOW_EXPERIMENT_DIR} exists." && aws --endpoint-url=$ENDPOINT s3 cp $MLFLOW_EXPERIMENT_DIR s3://$MLFLOW_BUCKET/ --recursive

###################### Dataset public ######################
aws --endpoint-url=$ENDPOINT s3 mb s3://$CITIBIKE_DATASET_BUCKET

# Public bucket
aws --endpoint-url=$ENDPOINT s3api put-bucket-policy --bucket $CITIBIKE_DATASET_BUCKET --policy file://$ZENML_INFRA_DIR/stacks/citibike-data-bucket-policy.json

# Restore cibibike datasets
echo "Restore datatset directory: ${MLFLOW_EXPERIMENT_DIR}"
[ -d "${PROCESSED_DATA_DIR}" ] && echo "Directory ${PROCESSED_DATA_DIR} exists." && aws --endpoint-url=$ENDPOINT s3 cp $PROCESSED_DATA_DIR s3://$CITIBIKE_DATASET_BUCKET/datasets/processed --recursive 