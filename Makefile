# Makefile

# Variables
ZENML_CONFIG_PATH = configs/zenml
DOCKER_COMPOSE_PATH = deployment/docker-compose
ZENML_INFRA_PATH = infra/zenml/stacks
ENV_FILE = .env


# Default target: start Docker Compose
.PHONY: install-base
install-base:
	@echo "Create buckets and Restore informations"
	zenml integration install s3 sklearn xgboost mlflow evidently bentoml

# Default target: start Docker Compose
.PHONY: setup-local
setup-local:
	@echo "Create buckets and Restore informations"
	sh ${ZENML_INFRA_PATH}/setup_local_stack.sh ${ENV_FILE}

# Default target: start Docker Compose
.PHONY: up
up:
	@echo "Starting Docker Compose with the $(ENV_FILE) file"
	docker-compose --file $(DOCKER_COMPOSE_PATH)/docker-compose.yaml --env-file $(ENV_FILE) up -d
	@echo "Create buckets and Restore informations"
	sh ${ZENML_INFRA_PATH}/localstack-setup.sh

# To stop the containers
.PHONY: down
down:
	@echo "Saving buckets to local"
	sh ${ZENML_INFRA_PATH}/localstack-backup.sh 
	@echo "Stopping Docker Compose"
	docker-compose --file $(DOCKER_COMPOSE_PATH)/docker-compose.yaml down


# To restart the containers
.PHONY: restart
restart:
	@echo "Restarting Docker Compose"
	docker-compose --file $(DOCKER_COMPOSE_PATH)/docker-compose.yaml --env-file $(ENV_FILE) down
	docker-compose --file $(DOCKER_COMPOSE_PATH)/docker-compose.yaml --env-file $(ENV_FILE) up -d


# Run the Python pipeline with two parameters
.PHONY: training
training:
	@echo "Running the training pipeline"
	python run.py --pipeline training --config_path $(ZENML_CONFIG_PATH)/pipelines.local.yaml

# Run the Python pipeline with two parameters
.PHONY: deploy-bentoml
deploy-bentoml:
	@echo "Running the deploy-bentoml pipeline"
	python run.py --pipeline deploy-bentoml --config_path $(ZENML_CONFIG_PATH)/pipelines.local.yaml

# Run the Python pipeline with two parameters
.PHONY: monitoring
monitoring:
	@echo "Running the monitoring pipeline"
	python run.py --pipeline monitoring --config_path $(ZENML_CONFIG_PATH)/pipelines.local.yaml