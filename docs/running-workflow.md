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


### **training**
This command executes the training pipeline defined in your [`run.py`](../run.py) file. It loads the training configuration from [`pipelines.local.yaml`](../configs/zenml/pipelines.local.yaml).

```bash
make training
```

In the zenml web console, go to the pipelines tab and select the one that starts with the name "citibike_training_pipeline". 

![image](images/zenml-pipeline-list-train.jpg)

We will be shown a list of all the executions of the training pipeline.

We select the most recent execution


This project uses mlflow to record experiments. The mlflow service runs at the following address [http://localhost:5000/](http://localhost:5000/).
It also uses mlflow to manage candidate models and promote them to production whenever the candidate's rmse exceeds the **threshold** defined in the [pipelines.local.yaml](configs/zenml/pipelines.local.yaml). The registered model 'xgb-citibike-reg-model' is shown below.

![image](images/zenml-pipeline-train-mflow-model-xgb-list.jpg)

Note that there are several versions of the resisted model 'xgb-citibike-reg-model'. The best model is tagged with the alias champion, and the 'stage' tag is used to track its status. In this case, the model with the alias champion and the 'production' tag is the best model according to the RMSE metric and has been promoted to production. You can also see that the other models have been tagged with the 'stage' tag and the value 'archived' to mark them as archived.

If we select the production model we can see that on its main page there is a link to its execution.

![image](images/zenml-pipeline-train-mflow-model-xgb.jpg)

On the registered model execution page, you can see the execution artifacts. You can also see that these artifacts are saved in a localstack bucket.

![image](images/zenml-pipeline-train-mflow-model-xgb-artifacts.jpg)



### **deploy-bentoml**
This command runs the deployment pipeline for BentoML, using the configuration from [`pipelines.local.yaml`](../configs/zenml/pipelines.local.yaml). This is where the trained models are packaged and deployed.

```bash
make deploy-bentoml
```

In the zenml web console, go to the pipelines tab and select the one that starts with the name "bentoml_deployment_pipeline".

![image](images/zenml-pipeline-list-deploy.jpg)

We will be shown a list of all the executions of the monitoring pipeline.

![image](images/zenml-pipeline-deploy-list.jpg)

We select the most recent execution

![image](images/zenml-pipeline-deploy-workflow.jpg)

By selecting the bentoml_model_deployer_step output, we can access the metadata tab where the address where the bentlo REST API service has been deployed will be shown.

![image](images/zenml-pipeline-deploy-metadata.jpg)


To view whether the bentoml REST API service has started correctly, type the following command:

```bash
zenml model-deployer models list
```

![image](images/zenml-pipeline-deploy-models-list.jpg)


The bentoml REST API service endpoint is located at the following address [http://127.0.0.1:3000/](http://127.0.0.1:3000/):

![image](images/zenml-pipeline-deploy-bentoml.jpg)

#### Troubleshooting


To view the REST API service logs with bentoml we must execute the following command.

```bash
zenml model-deployer models logs 155e16e0-fa12-421b-90ea-5ffb49275f34
```


There are times when the deployment may fail and ZenML may not be able to replace the REST API service correctly. To do this, we must delete the deployed model with the following commands.

We search for the identifier of the deployed model with the following command.

```bash
zenml model-deployer models list
```

We copy the identifier of the deployed model "UUID" and execute the following command to delete the deployed model.

```bash
zenml model-deployer models remove 155e16e0-fa12-421b-90ea-5ffb49275f34
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

A way of seeing data drifting is through the workflow and selecting the 'report_html' result from the 'evidently_report_step' step.

![image](images/zenml-pipeline-monitoring-evidently.jpg)


Another way to view monitoring is through a dashboard in Grafana. To do this, go to the following address [http://localhost:3030/dashboards](http://localhost:3030/dashboards).


![image](images/grafana-monitoring-list.jpg)

From the list of previous dashboards, we selected the "Monitoring: City Bike Trip Prediction" dashboard.

![image](images/grafana-monitoring.jpg)

### **test-integration**
This target runs the integration tests defined in the tests/integration directory using pytest.

```bash
make test-integration
```