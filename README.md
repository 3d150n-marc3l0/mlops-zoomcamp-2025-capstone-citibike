# mlops-zoomcamp-2025-capstone-citibike

![image](docs/images/citibike-banner.jpg)


## Introduction

The [Citibike system in New York City](https://citibikenyc.com/system-data) provides a convenient and sustainable mode of transportation for both residents and tourists. However, managing the system efficiently involves addressing several challenges, including optimizing bike availability, predicting demand across different areas, and minimizing system downtime.

Key challenges include:

- Bike Availability: Ensuring that bikes are available at stations where demand is highest, especially during peak hours.

- Usage Patterns: Understanding how weather, time of day, and special events affect bike usage.

- Maintenance and Downtime: Minimizing the time bikes are unavailable due to maintenance or malfunction.

Analyzing and predicting these patterns is crucial for improving the user experience and operational efficiency, reducing costs, and supporting the growth of bike-sharing systems as an eco-friendly alternative to traditional transportation.


### Objectives

The objective of this project is to build a predictive model for bike trips using the Citibike NYC dataset. The model will forecast the number of trips per hour, providing valuable insights into bike availability and demand. To achieve this, we seek to answer the following questions:

- How can we predict the number of bike trips per hour with the highest accuracy?
- What is the impact of weather data (e.g., temperature, precipitation) on bike trip predictions?
- How can we set up an MLOps ecosystem to ensure smooth model training, deployment, and monitoring?
- What are the best practices for building efficient training and deployment pipelines?
- How can we deploy the model as a REST API for real-time predictions?
- What methods can be used to monitor the model's performance and detect data drift over time?
- How can we implement best practices like unit testing, code formatting, and pre-commit hooks in the development process?


### Overview

This project aims to build a prediction model for bike trips using the Citibike NYC dataset. The model will forecast the number of trips per hour, providing valuable insights into bike availability and demand. After developing the predictive model, the project will focus on implementing an MLOps pipeline to manage the machine learning lifecycle, from model training and deployment to monitoring and maintenance.

To achieve this, the following tasks will be carried out:

- Predict the number of bike trips per hour: The goal is to develop a regression model to predict the number of trips for each hour of the day. This will provide insights for future bike availability, helping optimize the distribution of bikes across stations.

- Incorporate weather data: Weather conditions are expected to significantly influence bike usage. By integrating meteorological data into the model, we aim to improve the accuracy of predictions based on environmental factors such as temperature, precipitation, and wind speed.

- Set up an MLOps ecosystem: The project will focus on configuring a robust MLOps pipeline for the deployment and management of the regression model. This will ensure seamless training, versioning, and deployment processes.

- Develop training and deployment pipelines: We will design and implement efficient data pipelines for model training and deployment, ensuring scalability and automation throughout the machine learning lifecycle.

- Deploy the model and expose it via a REST API: Once the model is trained, it will be deployed in a production environment, where it will be accessible through a REST API for real-time predictions and integration with other systems.

- Monitor the model and detect data drift: After deployment, continuous monitoring will be implemented to track model performance. Data drift will be detected to ensure the model remains accurate and reliable over time.

- Implement best practices: The project will follow best practices, including unit testing, integrating linting and formatting tools (e.g., black, flake8), setting up pre-commit hooks, and creating a Makefile to streamline development and ensure code quality.

## Technologies

State-of-the-art software tools were used to carry out this project. These tools are briefly described below.

- **Python (3.12.3)**. [Python](https://www.python.org/) is a high-level, interpreted programming language widely used in data science, machine learning, and web development. Version 3.12.3 offers enhanced performance and new features for more efficient coding.

- **Poetry (2.1.3)**. [Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool that helps manage libraries and environments. It simplifies the process of declaring, installing, and updating dependencies in Python projects.

- **Poetry Shell**. The [`poetry shell`](https://github.com/python-poetry/poetry-plugin-shell) command activates a virtual environment managed by Poetry. It allows developers to work within an isolated environment, ensuring that dependencies do not conflict with other projects.

- **ZenML (0.83.1)**. [ZenML](https://www.zenml.io/) is an open-source machine learning (ML) pipeline library that enables reproducibility, collaboration, and automation of ML workflows. It helps in managing and tracking data, models, and experiments across pipelines.

- **MLflow (2.22.1)**. [MLflow](https://mlflow.org/) is an open-source platform for managing the machine learning lifecycle, including experimentation, reproducibility, and deployment. It supports tracking experiments, packaging code into reproducible runs, and managing models.

- **Optuna (3.6.2)**. [Optuna](https://optuna.readthedocs.io/en/stable/index.html#) is a hyperparameter optimization framework designed to automate the search for the best hyperparameters. It supports efficient and flexible optimization processes, ideal for machine learning model tuning.

- **XGBoost (3.0.3)**. [XGBoost](https://xgboost.readthedocs.io/en/stable/) is an optimized gradient boosting library designed for speed and performance. It is widely used for structured/tabular data and is highly effective in predictive modeling and machine learning competitions.

- **BentoML (1.4.19)**. [BentoML](https://www.bentoml.com/) is a flexible framework for serving, managing, and deploying machine learning models in production. It simplifies the process of packaging and deploying models as REST APIs or batch inference services.

- **Evidently (0.4.22)**. [Evidently](https://www.evidentlyai.com/) is an open-source tool designed for monitoring machine learning models and tracking their performance over time. It provides capabilities for visualizing model performance, detecting data drift, and understanding shifts in input data. It is highly useful for ensuring that models remain accurate and reliable once deployed, especially in production environments.

- **NumPy (1.26.4)**. [NumPy](https://numpy.org/) is a fundamental library for numerical computing in Python. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on them.

- **Scikit-learn (1.5.2)**. [Scikit-learn](https://scikit-learn.org/stable/) is a powerful Python library for machine learning, providing tools for data preprocessing, feature selection, and algorithms for classification, regression, clustering, and more.

- **LocalStack**. [LocalStack](https://github.com/localstack/localstack) is a fully functional local AWS cloud stack. It allows developers to run AWS services locally, which is useful for testing and development without incurring costs or requiring an internet connection.

- **Docker**. [Docker](https://www.docker.com/) is a platform used to develop, ship, and run applications in containers. It allows for consistent environments across different stages of development and production, making it easier to deploy and scale applications.

- **Grafana**. [Grafana](https://grafana.com/) is an open-source visualization and monitoring platform that integrates with various data sources. It is commonly used for monitoring and visualizing machine learning model performance, logs, and metrics.

- **Docker-compose**. [Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. It allows developers to manage complex setups and services in an easy-to-use YAML configuration.

- **Pytest (8.4.1)**. [Pytest](https://docs.pytest.org/en/stable/) is a testing framework for Python that enables writing simple and scalable test cases. It supports fixtures, parameterized testing, and rich plugins, making it an essential tool for unit and integration testing in Python projects.

- **Black (25.1.0)**. [Black](https://github.com/psf/black) is an uncompromising Python code formatter. It automatically formats Python code to adhere to PEP 8 standards, promoting consistency and improving readability across teams.

- **Flake8 (7.3.0)**. [Flake8](https://flake8.pycqa.org/en/latest/) is a tool for checking the style guide enforcement and linting in Python code. It combines various linters to check for errors, unused code, and other violations of Python coding standards.

- **Pre-commit**. [Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks. It automates code quality checks, including linting and formatting, before code is committed to version control, ensuring that code adheres to best practices.


## Datasets

This project uses two primary datasets:

- **CitiBike NYC Dataset**: This dataset contains information about bike trips made by users of the Citi Bike system in New York City. It includes details such as trip duration, start and end stations, ride types, and user membership information. This data helps analyze usage patterns and predict bike availability.

- **NOAA Weather Data**: This dataset provides historical weather information from the National Oceanic and Atmospheric Administration (NOAA). It includes various weather parameters such as temperature, precipitation, wind speed, and snow data, which are used to improve the accuracy of bike trip predictions by factoring in weather conditions.

For detailed descriptions of these datasets, please refer to the [Datasets Documentation](docs/datasets.md).



### Environment Setup

This project requires certain tools and configurations to run correctly. You must ensure that Python 3.12, Docker, and Docker Compose are installed. Additionally, **Poetry** and **Poetry Shell** are used for dependency management and creating isolated environments.

For detailed instructions on how to configure the environment and install the necessary tools, please refer to the [Environment Setup Guide](docs/config-environment.md).



## Settings

### Local Setting up

### Dependency management

This project uses the poetry tool for dependency management and packaging in Python. Therefore, this section explains the tool's installation and the project's library dependencies.



#### Installing Poetry

To install poetry, use the installation script available directly at install.python-poetry.org. You can run the script by typing the following command.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Open your shell configuration file:
Depending on the shell you're using, you'll need to modify a configuration file:

- **Bash**: If you're using Bash, open the ~/.bashrc or ~/.bash_profile file.

- **Zsh**: If you're using Zsh, open the ~/.zshrc file.

- **Fish**: If you're using Fish, open the ~/.config/fish/config.fish file.

For example, in shell option you have to open your shell configuration file (~/.bashrc) and 
add `export PATH="/home/emmuzoo/.local/bin:$PATH"` to your shell configuration file.

```bash
vi ~/.bashrc
...
...
...

export PATH="/home/emmuzoo/.local/bin:$PATH"
```

After editing the file, apply the changes without having to close and reopen the terminal with:

```bash
source ~/.bashrc
```

You can test that everything is set up by executing:

```bash
poetry --version

Poetry (version 2.1.3)
```
```bash
which python3.11

/usr/bin/python3.11
```

```bash
poetry env use /usr/bin/python3.11
```

#### Installing pyenv

By default, Poetry will try to use the Python version used during Poetry’s installation to create the virtual environment for the current project.

```bash
curl -fsSL https://pyenv.run | bash
```


```bash
sudo apt update
sudo apt install -y libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```



```bash
pyenv install 3.11.13
```

Activate Python 3.11 for the current project

```bash
pyenv local 3.11.13  # Activate Python 3.9 for the current project
```

```bash
python --version
Python 3.11.13
```

```bash
poetry env use $(pyenv which python)
```

```bash
poetry env use $(pyenv which python)
Using virtualenv: /home/emmuzoo/.cache/pypoetry/virtualenvs/mlops-zoomcamp-2025-capstone-citibike-_1VljUqA-py3.11
```

```bash
poetry install
```


#### Installing dependencies

```bash
poetry install
```

#### Installing Poetry Shell

The poetry shell command is used to spawn a new shell within the virtual environment created by Poetry for your project. This allows you to run commands and scripts within the virtual environment without having to manually activate it each time. To make things easier, Poetry Shell will be installed. To do so, run the following command:

```bash
poetry self add poetry-plugin-shell
```
Once 'poetry shell' is installed, we launch a new shell (command interpreter) within that environment using the following command.

```bash
poetry shell
```
The above command will have an output similar to the following output.

```bash
(mlops-zoomcamp-2025-capstone-citibike-py3.12) emmuzoo@DESKTOP-RUSHFLK:~/mlops-zoomcamp-2025-capstone-citibike$ 
```

You can test that everything is set up by executing:

```bash
python 
Python 3.12.3 (main, Jun 18 2025, 17:59:45) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

### Setting With Poetry

```bash
cd ~/mlops-zoomcamp-2025-capstone-citibike
poetry init
```

 Install dependecies:
```bash
poetry add --group dev $(cat requirements.dev.txt)
```

```bash
poetry add $(cat requirements.txt)

```

# Experiments
## Notebooks

To run jupyter lab you have to type the following commands:

```bash
cd notebooks/
poetry run python jupyter lab
```


## Run

### Run local

To run locally, a docker-compose build was created, defining several services used during the execution of the pipelines in zenml.

For ease of use, a makefile was created with the following operations:

- up. Starts the services defined in docker-compose. Once localstack is started, it creates the buckets and restores the experiment information, if any.

- down. Backs up the information contained in the localstack buckets to the experiment directory. Then, stop the services defined in docker-compose.


### Run docker-compose 

To start the services defined in docker-compose we must execute the following command.

```batch
make up
```
We check that the services have started correctly by executing the following command.

```batch
docker ps -a
```

As a result, we will obtain a list of containers that represent the services defined in the docker-compose file and its result should look like the following:

```batch
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS                    PORTS                                                          NAMES
3b198eed3915   ghcr.io/mlflow/mlflow:latest      "/bin/sh -c 'python3…"   38 minutes ago   Up 37 minutes             0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp                    mlflow
7e355152de07   zenmldocker/zenml-server:0.83.1   "/entrypoint.sh uvic…"   38 minutes ago   Up 38 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp                    zenml
26dff654ba11   localstack/localstack             "docker-entrypoint.sh"   38 minutes ago   Up 38 minutes (healthy)   127.0.0.1:4510-4559->4510-4559/tcp, 127.0.0.1:4566->4566/tcp   localstack
c5993f3cd026   postgres:15                       "docker-entrypoint.s…"   38 minutes ago   Up 38 minutes             0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                    mlflow-db
537732dd3ee3   postgres:15                       "docker-entrypoint.s…"   38 minutes ago   Up 38 minutes             0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp                    grafana-db
2b8fc8b9d60e   grafana/grafana-enterprise        "/run.sh"                38 minutes ago   Up 38 minutes             0.0.0.0:3030->3000/tcp, [::]:3030->3000/tcp                    grafana
e6b5c933cd6f   mysql:8.0                         "docker-entrypoint.s…"   38 minutes ago   Up 38 minutes             0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp                    zenml-db
```

### Login in Zenml

Once the orchestration is started, we need to log in from the command line, to do this we execute the following command:

```batch
zenml login http://localhost:8080
```

The previous command provides us with a URL that we must type into a browser to authorize our machine to run pipeline.



### Down docker-compose

To stop the services defined in docker-compose we must execute the following command.

```batch
make down
```
We check that the services have started correctly by executing the following command.

```batch
docker ps -a
```
The above command should not show any containers.

## Reproducibility