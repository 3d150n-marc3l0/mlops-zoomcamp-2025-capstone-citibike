# Architecture

This section describes the architecture of the project modules.

## Directory Structure
The project follows a well-organized directory structure, where each folder and file serves a specific purpose within the ZenML, MLflow, BentoML, and data processing workflow.


```textplain
.
├── configs
│   └── zenml
├── data
│   ├── processed
│   ├── raw
│   ├── stag
│   └── test
├── deployment
│   ├── bentoml
│   └── docker-compose
├── docs
│   ├── images
│   ├── config-environment.md
│   ├── datasets.md
│   ├── running-workflow.md
│   └── technology-stack.md
├── experiments
│   ├── mflow
│   └── zenml
├── infra
│   └── zenml
├── notebooks
│   ├── EDA.ipynb
│   ├── Monitoring.ipynb
│   └── Training.ipynb
├── pipelines
│   ├── __pycache__
│   ├── __init__.py
│   ├── deployment.py
│   ├── monitoring.py
│   └── training.py
├── steps
│   ├── __pycache__
│   ├── __init__.py
│   ├── data_loaders.py
│   ├── data_validator.py
│   ├── hpo_tuner.py
│   ├── inference_predict.py
│   ├── model_deployer.py
│   ├── model_evaluator.py
│   ├── model_monitor.py
│   ├── model_promoter.py
│   ├── model_register.py
│   ├── model_trainer.py
│   ├── model_validator.py
│   └── notify_on.py
├── tests
│   ├── integration
│   ├── unit
│   └── test.py
├── utils
│   ├── __pycache__
│   ├── __init__.py
│   ├── promotion_helper.py
│   └── tracker_helper.py
├── LICENSE
├── Makefile
├── README.md
├── poetry.lock
├── pyproject.toml
├── run.py
```

## Directory Breakdown:
1. `configs/zenml/`:

    - Contains ZenML configuration files necessary to define the pipeline and integration settings.

2. `data/`:

    - Holds the project’s datasets.

        - `raw/`: The raw, unprocessed data.

        - `processed/`: Data that has been preprocessed and cleaned.

        - `stag/`: Staging area for data that is being prepared for final use.

        - `test/`: A subset of the data used for testing models.

3. `deployment/`:

    - Contains deployment-related files.

        - `bentoml/`: BentoML related configurations for deploying models as REST APIs.

        - `docker-compose/`: Docker Compose configurations for managing the containers and services.

4. `docs/`:

    - Contains documentation files.

        - `images/`: Folder for images used within the documentation.

        - `config-environment.md`: Documentation for setting up the environment.

        - `datasets.md`: Describes the datasets used within the project.

        - `running-workflow.md`: Details on running the ZenML-based workflow.

        - `technology-stack.md`: Describes the technology stack used in the project.

5. `experiments/`:

    - Stores experiment-related files.

        - `mflow/`: Files related to MLflow experiments.

        - `zenml/`: Files related to ZenML experiments.

6. `infra/`:

    - Contains infrastructure configuration files for ZenML and the overall system setup.

        - `zenml/`: Files related to setting up ZenML integrations and stacks.

7. `notebooks/`:

    - Jupyter notebooks used for exploratory analysis and model training.

        - `EDA.ipynb`: Notebook for Exploratory Data Analysis (EDA).

        - `Monitoring.ipynb`: Notebook for monitoring model performance and calculating drift.

        - `Training.ipynb`: Notebook for executing model training and hyperparameter optimization (HPO).

8. `pipelines/`:

    - Contains Python files defining various pipelines.

        - `deployment.py`: Defines the model deployment pipeline.

        - `monitoring.py`: Defines the pipeline for monitoring data and model drift.

        - `training.py`: Defines the pipeline for model training and hyperparameter optimization (HPO).

9. `steps/`:

    - Contains Python files for different steps involved in the ML workflow.

        - `data_loaders.py`: Script for loading and preprocessing data.

        - `data_validator.py`: Validates the integrity of the data.

        - `hpo_tuner.py`: Tunes hyperparameters using optimization algorithms like Optuna.

        - `inference_predict.py`: Handles model inference and predictions.

        - `model_deployer.py`: Deploys models into production using BentoML.

        - `model_evaluator.py`: Evaluates the performance of trained models.

        - `model_monitor.py`: Monitors models for performance or data drift.

        - `model_promoter.py`: Promotes models that meet the criteria into production.

        - `model_register.py`: Registers models with MLflow for versioning and tracking.

        - `model_trainer.py`: Trains the models using the selected data.

        - `model_validator.py`: Validates the models before deployment.

        - `notify_on.py`: Handles notifications for various stages (e.g., model promotion, failure).

10. `tests/`:

    - Stores test files for unit and integration tests.

        - `integration/`: Contains integration tests for the entire pipeline or components.

        - `unit/`: Contains unit tests for individual modules or functions.

        - `test.py`: General test script for running various test cases.

11. `utils/`:

    - Contains utility scripts for various helper functions.

    - `promotion_helper.py`: A utility script for promoting models in the pipeline.

    - `tracker_helper.py`: Helps with tracking experiments, models, and metrics.

12. Root Files:

    - `LICENSE`: License file for the project.

    - `Makefile`: Defines various operations like installing dependencies, setting up Docker, and running the pipeline.

    - `README.md`: Provides an overview of the project, its structure, and how to use it.

    - `poetry.lock`: Lock file for Python dependency management.

    - `pyproject.toml`: Project configuration file for managing dependencies and packaging with Poetry.

    - `run.py`: Main entry point to run different parts of the pipeline.




## Description of the Pipelines

1. [training.py](../pipelines/training.py):

- This script handles the model training and hyperparameter optimization (HPO). It performs the following tasks:

    - `Feature Engineering`: New features are created and transformed to improve the model's performance.

    - `Feature Selection`: The most relevant features are selected based on various selection techniques.

    - `Hyperparameter Optimization (HPO)`: Methods like Optuna are used to tune the model’s hyperparameters.

    - `Model Promotion`: If the trained model (candidate) improves the current production model (champion) by at least a defined threshold of RMSE, the candidate becomes the new champion (production model). If the candidate does not outperform the champion, it is archived.

        - If the candidate model improves the champion model, the champion model is archived, and the candidate model becomes the production model with the tag stage=production.

2. [deployment.py](../pipelines/deployment.py):

    - This script is responsible for deploying the model to production:

    - It uses MLflow to fetch the model that has been promoted to production (tagged as stage=production and alias champion).

    - The model is then deployed as a REST API service using BentoML, allowing other systems to interact with the model through HTTP requests.

3. [monitoring.py](../pipelines/monitoring.py):

    - This script takes care of monitoring the model in production:

    - It calculates data drift and model drift by comparing data from 2024 and the first three months of 2025.

    - The drift calculation is done using the Evidently library, which provides metrics and statistics for model and data drift.

    - Drift metrics are saved into a database for later analysis.

    - Grafana is connected to this database to display a dashboard that visualizes the drift of the model and other key metrics, such as the number of features and missing values in the data.


## Setting of Pipelines


Each pipeline has its own configuration. To facilitate the management of these parameters, the [configs/zenml/pipelines.local.yaml](configs/zenml/pipelines.local.yaml) file has been created. This file contains the configuration for each pipeline. The parameters for each pipeline are explained below.

### Training Pipeline Setting

Parameters:
- `data_url`: URL for the processed data used for training. Default is set to http://localhost:4566/citibike-data/datasets/processed/.

- `start_train_date`:  Start date for training data. Default is 2025-01-01.

- `end_train_date`:  End date for training data. Default is 2025-12-31.

- `test_size`: Fraction of the dataset to be used as test data. Default is 0.2 (20%).

- `shuffle`: Whether to shuffle the data before splitting into training and testing sets. Default is True.

- `random_state`: Seed for random number generator used in splitting the data. Default is 42.

- `n_trials`: Number of trials for Hyperparameter Optimization (HPO) using Optuna. Default is 50.

- `registered_model_name`: The name of the registered model in MLflow. Default is "xgb-citibike-reg-model".

- `threshold`: The threshold value for model promotion based on RMSE improvement compared to the current production model. Default is 0.1 (10%).

### Deploy-BentoML Pipeline Setting

Parameters:
- `model_name`: Name of the model to be deployed, typically the best model (champion). Default is "xgb-citibike-reg-model".

- `model_alias`: Alias for the model in the BentoML service. Default is "champion".

- `service_class`: Path to the BentoML service class that will be used for deployment. Default is "service.py:CitibikeService".

- `working_dir`: Directory where the BentoML service files are located. Default is "./deployment/bentoml".

- `image_name`: Docker image name for the deployed service. Default is "mlop-zoomcamp-citibike".

- `image_tag`: Docker image tag for versioning the deployed service. Default is "0.1.0".

- `packages`: List of required Python packages for the BentoML service. Defaults are provided for all dependencies needed to run the service:

    - `"zenml==0.83.1"

    - `"mlflow==2.22.1"

    - `"numpy==1.26.4"

    - `"pandas==2.3.1"

    - `"psutil==5.9.8"

    - `"scikit-learn==1.7.0"

    - `"scipy==1.16.0"

    - `"xgboost==3.0.2"

    - `"holidays==0.77"


### Monitoring Pipeline

Parameters:
- `data_url`: URL for the processed data used for monitoring. Default is http://localhost:4566/citibike-data/datasets/processed/.

- `model_name`: The model to monitor for drift. Default is "xgb-citibike-reg-model".

- `model_alias`: Alias for the model being monitored. Default is "champion".

- `host`: Hostname of the monitoring database. Default is "monitoring-db".

- `port`: Port of the monitoring database. Default is 5433.

- `database`: Name of the monitoring database. Default is "monitoring".

- `start_reference_date`: Start date of the reference data (used for comparison). Default is 2024-01-01.

- `end_reference_date`: End date of the reference data. Default is 2024-03-31.

- `start_current_date`: Start date for the current data (to check against the reference data). Default is 2025-01-01.

- `end_current_date`: End date for the current data. Default is 2025-03-31.


## Run pipelines

The [`run.py`](../run.py) module is responsible for calling the various pipelines. Its operation and the different supported pipelines are described below.

### General Functionality:
1. Command-Line Interface (CLI):

    - The script uses Click to define a simple CLI interface. You can pass in the name of the pipeline you want to execute (e.g., training, deploy-bentoml, monitoring) along with the path to a configuration file (config_path).

    - The CLI options are:

        - `--pipeline`: Specifies which pipeline to run.

        -  `--config_path`: Specifies the path to the configuration file (typically pipelines.local.yaml).

2. Read Configuration File:

    - The read_config function reads the YAML configuration file, which contains the parameters for each pipeline.

    - It loads the YAML file using yaml.safe_load and then returns the configuration as a dictionary.

3. Pipeline Execution:

    - Based on the pipeline argument passed through the command line, the script dynamically selects the appropriate pipeline function to run (such as citibike_training_pipeline, bentoml_deployment_pipeline, etc.).

    - Each pipeline function is called with the corresponding parameters read from the configuration file.

4. Pipeline Validation:

    - For each pipeline, the script ensures that the parameters key exists in the configuration for that pipeline. If not, it raises an error.

### Supported Pipelines:
1. Training Pipeline (`training`):

    - **Description**: This pipeline performs model training, feature engineering, feature selection, and hyperparameter optimization (HPO).

    - **Function**: It calls the citibike_training_pipeline function, passing the parameters from the pipelines.local.yaml file.

2. BentoML Deployment Pipeline (`deploy-bentomlp`):

    - **Description**: This pipeline is responsible for deploying the model as a REST API using BentoML.

    - **Function**: It calls `bentoml_deployment_pipeline` with the deployment parameters from the configuration file.

3. Monitoring Pipeline (`monitoring`):

    - **Description**: This pipeline is used to monitor model performance over time, detecting model drift using Evidently.

    - **Function**: It calls `batch_monitoring_backfill`, passing the parameters from the config file to fetch relevant data for monitoring and calculating drift.




## Storage: Buckets

In this project, it is used as remote storage in LocalStack by Mflow, Zenml, and the pipelines.

The `mlflow-artifact`s bucket is created for use by Mflow. Mflow uses this bucket to store artifacts from experiments performed during the training pipeline or in experiments performed with notebooks.

The `zenml-artifacts` bucket is created for use by Zenml. Zenml uses this bucket to store logs or artifacts generated during the execution of the pipelines.

The `citibike-data` bucket is created to store the training and test datasets. The datasets are used by the different pipelines. The contents of this bucket are shown below.

```textplain
citibike-data
├── datasets
    ├── processed
        ├── citibike
        │   ├── 2024-citibike-tripdata.parquet
        │   └── 2025-citibike-tripdata.parquet
        └── weather
            ├── 2024-weather.parquet
            └── 2025-weather.parquet
```

The `citibike-data/datasets/processed/citibike` directory stores processed datasets of NYC Citibike trips. Mientras, the `citibike-data/datasets/processed/weather` directory stores the processed weather datasets for New York City.