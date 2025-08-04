#!/bin/sh
echo "Backup: Downloading from localstack s3 to local"

ENDPOINT=http://localhost:4566  # LOCALSTACK
#ENDPOINT=http://localhost:9000  # MINIO

# Experiment directorory
EXPERIMENT_DIR=$PWD/experiments

# Buckets S3 in localstack
ZENML_BUCKET=zenml-artifacts            # zenml bucket
MLFLOW_BUCKET=mlflow-artifacts          # mlflow bucket
CITIBIKE_DATASET_BUCKET=citibike-data   # citibike datasets bucket


###################### ZenML ######################
echo "Saving to $EXPERIMENT_DIR/zenml"
aws --endpoint-url $ENDPOINT s3 cp s3://$ZENML_BUCKET/ $EXPERIMENT_DIR/zenml --recursive

###################### Mlfow ######################
echo "Saving to $EXPERIMENT_DIR/mflow"
aws --endpoint-url $ENDPOINT s3 cp s3://$MLFLOW_BUCKET/ $EXPERIMENT_DIR/mflow --recursive