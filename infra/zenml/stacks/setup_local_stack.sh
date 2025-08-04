#!/usr/bin/env bash


# Verificar si se proporcionó un archivo .env
if [ -z "$1" ]; then
  echo "Error: Debes proporcionar un archivo .env como parámetro."
  exit 1
fi

# Cargar las variables del archivo .env proporcionado
export $(grep -v '^#' "$1" | xargs)


#set -Eeo pipefail
set -Ee pipefail


# Store the AWS access key in a ZenML secret
zenml secret create pg_monitoring_secret \
    --MONITORING_DB_USER="$MONITORING_DB_USER" \
    --MONITORING_BD_PASSWORD="$MONITORING_BD_PASSWORD"

# Data validator: evidently
#zenml data-validator register deepchecks_data_validator --flavor=deepchecks
zenml data-validator register evidently_data_validator --flavor=evidently

# Tracker model: mlflow
#zenml experiment-tracker register local_mlflow_tracker  --flavor=mlflow
zenml experiment-tracker register local_mlflow_tracker \
  --flavor=mlflow \
  --tracking_uri=http://mlflow:5000 \
  --tracking_username=dummy \
  --tracking_password=dummy

# Store the AWS access key in a ZenML secret
zenml secret create s3_secret \
    --aws_access_key_id="$AWS_ACCESS_KEY_ID" \
    --aws_secret_access_key="$AWS_SECRET_ACCESS_KEY"

# Storage local
zenml artifact-store register localstack_store -f s3 \
    --path="s3://zenml-artifacts" \
    --authentication_secret=s3_secret \
    --client_kwargs='{"endpoint_url": "http://localstack:4566", "region_name": "eu-west-1"}'


# Mode registry: mlflow
zenml model-registry register local_mlflow_registry --flavor=mlflow

# Deploy model
zenml model-deployer register local_mlflow_deployer  --flavor=mlflow
zenml model-deployer register local_bentoml_deployer --flavor=bentoml

# Register stack
zenml stack register local_citibike_stack \
    -a localstack_store \
    -o default \
    -e local_mlflow_tracker \
    -r local_mlflow_registry \
    -d local_bentoml_deployer \
    -dv evidently_data_validator

# Set new stack like a defaul
zenml stack set local_citibike_stack