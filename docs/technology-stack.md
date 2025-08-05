# Technology Stack

This project utilizes a variety of modern technologies and tools to facilitate development, deployment, and management of the machine learning pipeline. Below is an overview of each of these tools.

## Core Technologies

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

## Infrastructure and Monitoring

- **LocalStack**. [LocalStack](https://github.com/localstack/localstack) is a fully functional local AWS cloud stack. It allows developers to run AWS services locally, which is useful for testing and development without incurring costs or requiring an internet connection.
- **Docker**. [Docker](https://www.docker.com/) is a platform used to develop, ship, and run applications in containers. It allows for consistent environments across different stages of development and production, making it easier to deploy and scale applications.
- **Grafana**. [Grafana](https://grafana.com/) is an open-source visualization and monitoring platform that integrates with various data sources. It is commonly used for monitoring and visualizing machine learning model performance, logs, and metrics.
- **Docker-compose**. [Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. It allows developers to manage complex setups and services in an easy-to-use YAML configuration.

## Development and Best Practices

- **Pytest (8.4.1)**. [Pytest](https://docs.pytest.org/en/stable/) is a testing framework for Python that enables writing simple and scalable test cases. It supports fixtures, parameterized testing, and rich plugins, making it an essential tool for unit and integration testing in Python projects.
- **Black (25.1.0)**. [Black](https://github.com/psf/black) is an uncompromising Python code formatter. It automatically formats Python code to adhere to PEP 8 standards, promoting consistency and improving readability across teams.
- **Flake8 (7.3.0)**. [Flake8](https://flake8.pycqa.org/en/latest/) is a tool for checking the style guide enforcement and linting in Python code. It combines various linters to check for errors, unused code, and other violations of Python coding standards.
- **Pre-commit**. [Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks. It automates code quality checks, including linting and formatting, before code is committed to version control, ensuring that code adheres to best practices.

  
---

For a detailed description of how these technologies are configured and used in this project, please refer to the [README](../README.md).
