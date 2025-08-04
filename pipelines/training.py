from typing import Optional
import datetime
from zenml import pipeline
from zenml.logger import get_logger
from zenml.integrations.mlflow.steps.mlflow_registry import (
    mlflow_register_model_step,
)
from steps import (
    data_loader,
    data_splitter,
    citibike_data_report,
    citibike_data_test,
    data_preprocessor,
    optimize_hyperparams,
    xgb_trainer,
    model_scorer,
    register_model,
    promote_models,
    notify_on_success
)


logger = get_logger(__name__)



@pipeline
def citibike_training_pipeline(
    data_url: str = "http://localhost:4566/citibike-data/datasets/processed/",
    start_train_date: str = "2025-01-01", 
	end_train_date: str = "2025-12-31", 
    test_size: float = 0.2,
    shuffle: bool = True,
    random_state: int = 42,
    n_trials: int = 50,
    registered_model_name: str = "xgb-citibike-reg-model"
):
    logger.info("train pipeline")
    logger.info(f"start_train_date: {start_train_date}, test_size: {end_train_date}")
    start_train_date = datetime.datetime.strptime(start_train_date, "%Y-%m-%d")
    end_train_date = datetime.datetime.strptime(end_train_date, "%Y-%m-%d")

    ########## ETL stage ##########
    # Load dataset
    raw_data, target = data_loader(
        base_url=data_url,
        start_date=start_train_date,
        end_date=end_train_date
    )

    # Split data
    train, test = data_splitter(
        dataset=raw_data,
        test_size=test_size,
        shuffle=shuffle,
        random_state=random_state
    )

    # Preprocess data
    train = data_preprocessor(train)
    test = data_preprocessor(test)

    ########## validation data stage ##########

    json_report, html_report = citibike_data_report(
        reference_dataset=train,
        comparison_dataset=test,
    )
    
    json_report, html_report = citibike_data_test(
        reference_dataset=train,
        comparison_dataset=test,
        after=["evidently_report_step"]
    )

    ########## Hyperparameter tuning stage ##########
    
    best_params = optimize_hyperparams(
        train, 
        target, 
        n_trials=n_trials,
        after=["evidently_test_step"]
    )

    ########## Training stage ##########

    model = xgb_trainer(
        train, 
        target, 
        best_params
    )
    
    test_metrics = model_scorer(
        model, 
        train, 
        target
    )

    ########## Evaluation model stage ##########
    

    ########## Promotion stage ##########
    register_model(
        model,
        test_metrics,
        test,
        target,
        model_name=registered_model_name,
        after=["model_scorer"]
    )

    #mlflow_register_model_step
    is_promoted = promote_models(
        model_name=registered_model_name,
        after=["register_model"]
    )


    notify_on_success(is_promoted)