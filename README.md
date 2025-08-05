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

## Technology Stack

This project leverages a diverse set of technologies to support the development and deployment of machine learning models, containerization, and monitoring. For a detailed overview of the tools and libraries used, please refer to the [Technology Stack Documentation](docs/technology-stack.md).


## Datasets

This project uses two primary datasets:

- **CitiBike NYC Dataset**: This dataset contains information about bike trips made by users of the Citi Bike system in New York City. It includes details such as trip duration, start and end stations, ride types, and user membership information. This data helps analyze usage patterns and predict bike availability.

- **NOAA Weather Data**: This dataset provides historical weather information from the National Oceanic and Atmospheric Administration (NOAA). It includes various weather parameters such as temperature, precipitation, wind speed, and snow data, which are used to improve the accuracy of bike trip predictions by factoring in weather conditions.

For detailed descriptions of these datasets, please refer to the [Datasets Documentation](docs/datasets.md).



## Environment Setup

This project requires certain tools and configurations to run correctly. You must ensure that Python 3.12, Docker, and Docker Compose are installed. Additionally, **Poetry** and **Poetry Shell** are used for dependency management and creating isolated environments.

For detailed instructions on how to configure the environment and install the necessary tools, please refer to the [Environment Setup Guide](docs/config-environment.md).



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