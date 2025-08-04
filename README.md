# mlops-zoomcamp-2025-capstone-citibike
mlops-zoomcamp 2025 capstone
# de-zoomcamp-2025-capstone-baywheels

## Introduction

### Objectives

### Overview



## Technologies

- **Poetry**.
- **Zenml**.
- **Mlflow**.
- **Optuna**.
- **Bentoml**.
- **localstack**.


## Dataset



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