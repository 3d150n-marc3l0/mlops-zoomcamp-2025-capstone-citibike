# Running Workflow


# Running with Docker-Compose
The easiest way to run the application is with docker-compose.


### **up**
This command starts the Docker Compose services in the background using the docker-compose.yaml file and the .env file. It then runs the localstack-setup.sh script to configure LocalStack (which simulates AWS services locally).

```bash
make up
```

After starting ZenML with make up, use the following command to list all Docker containers:

```bash
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
e6b5c933cd6f   mysql:8.0                         "docker-entrypoint.s…"   38 minutes ago   Up 38 minutes             0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp  
```

Once the orchestration has started, We log in to the web console which is at the following address [shttp://localhost:8080/login](http://localhost:8080/login). 

![image](images/zenml-login.jpg)



###  **down**
This command stops all Docker Compose containers and saves the current LocalStack state (e.g., buckets and configurations) by running localstack-backup.sh. This ensures that the state is preserved when the containers are stopped.

```bash
make down
```


### **training***
This command executes the training pipeline defined in your [`run.py`](../run.py) file. It loads the training configuration from [`pipelines.local.yaml`](../configs/zenml/pipelines.local.yaml) in the specified ZENML_CONFIG_PATH.

```bash
make training
```


### **deploy-bentoml**
This command runs the deployment pipeline for BentoML, using the configuration from [`pipelines.local.yaml`](../configs/zenml/pipelines.local.yaml). This is where the trained models are packaged and deployed.

```bash
make deploy-bentoml
```


### **monitoring**
This operation runs the monitoring pipeline, using the configuration from [`pipelines.local.yaml`](../configs/zenml/pipelines.local.yaml), which typically involves checking the model's performance in production, tracking metrics, and possibly detecting data drift.

```bash
make monitoring
```

In the zenml web console, go to the pipelines tab and select the one that starts with the name "batch_monitoring_backfill".

![image](images/zenml-pipeline-list-monitoring.jpg)


We will be shown a list of all the executions of the monitoring pipeline.

![image](images/zenml-pipeline-monitoring-list.jpg)

We select the most recent execution

![image](images/zenml-pipeline-monitoring-workflow.jpg)

The second way to see data drifting is through the workflow and selecting the 'report_html' result from the 'evidently_report_step' step.

![image](images/zenml-pipeline-monitoring-evidently.jpg)


To view model monitoring, there are two ways. The first is through Grafana. To do this, go to the following address [http://localhost:3030/dashboards](http://localhost:3030/dashboards).


![image](images/grafana-monitoring-list.jpg)

From the list of previous dashboards, we selected the "Monitoring: City Bike Trip Prediction" dashboard.

![image](images/grafana-monitoring.jpg)

### **test-integration**
This target runs the integration tests defined in the tests/integration directory using pytest.

```bash
make test-integration
```