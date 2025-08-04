import time
from datetime import datetime, date, timedelta
import pandas as pd
from typing import Tuple, Annotated, List
import xgboost as xgb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric, RegressionQualityMetric
from zenml.client import Client
from zenml import pipeline, step
from zenml.logger import get_logger
from steps.data_validator import DATASET_CATEGORICAL_COLUMNS, DATASET_NUMERICAL_COLUMNS, DATASET_TARGET_COLUMN_NAME
from steps import (
     reference_data_loader,
     get_model_by_alias,
     data_preprocessor,
	 citibike_data_drift_report,
	 inference_predict,
)

# Base de datos para los modelos de SQLAlchemy
Base = declarative_base()

logger = get_logger(__name__)

SEND_TIMEOUT = 10

def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

# Definimos el modelo de la tabla citibike_metrics
class CitibikeMetrics(Base):
    __tablename__ = 'citibike_metrics'
    
    timestamp = Column(DateTime, primary_key=True)
    prediction_drift = Column(Float)
    num_drifted_columns = Column(Integer)
    share_missing_values = Column(Float)

    # Métricas de RegressionQualityMetric
    r2_score_reference = Column(Float)
    r2_score_current = Column(Float)
    rmse_score_reference = Column(Float)
    rmse_score_current = Column(Float)
    mae_score_reference = Column(Float)
    mae_score_current = Column(Float)
    mean_error_reference = Column(Float)
    mean_error_current = Column(Float)
    abs_error_max_reference = Column(Float)
    abs_error_max_current = Column(Float)
    mean_abs_perc_error_reference = Column(Float)
    mean_abs_perc_error_current = Column(Float)
    
    # Métricas de subrendimiento
    underperformance_mean_error = Column(Float)
    underperformance_std_error = Column(Float)
    underestimation_mean_error = Column(Float)
    underestimation_std_error = Column(Float)
    overestimation_mean_error = Column(Float)
    overestimation_std_error = Column(Float)
    
    # Desviaciones estándar de los errores
    error_std_reference = Column(Float)
    error_std_current = Column(Float)
    abs_error_std_reference = Column(Float)
    abs_error_std_current = Column(Float)
    abs_perc_error_std_reference = Column(Float)
    abs_perc_error_std_current = Column(Float)

# Crear la tabla en PostgreSQL si no existe
@step(
	enable_cache=False
)
def create_table_step(
    host: str,
    port: int,
    database: str
):
    """
    Este paso asegura que la tabla 'citibike_metrics' exista en la base de datos.
    """
	# Configuración de SQLAlchemy
    secret = Client().get_secret("pg_monitoring_secret")
    DATABASE_URL = f'postgresql://{secret.secret_values["MONITORING_DB_USER"]}:{secret.secret_values["MONITORING_BD_PASSWORD"]}@{host}:{port}/{database}'
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    logger.info("Tabla 'citibike_metrics' verificada o creada exitosamente.")
    

@step(
	enable_cache=False
)
def calculate_drift_metrics_step(
    reference_data: pd.DataFrame, 
    current_data: pd.DataFrame, 
	target: str,
	prediction: str,
	categorical_feats: List[str] = [],
	numerical_feats: List[str] = []
) -> Annotated[pd.DataFrame, "metrics"]:
	"""
	Este paso calcula las métricas de drift usando Evidently (model drift, column drift, missing values).
	"""
	# Calculate predictions
	logger.info(f"Calculate predictions")
	feats = categorical_feats + numerical_feats
	feats = feats if len(feats) else reference_data.columns
	current_data['week'] = current_data.index.isocalendar().week

	metric_list = []
	'''
	start_date = current_data.index.min()
	end_date = current_data.index.max()
	for current_date in daterange(start_date, end_date):
		# Filtrar los datos actuales para el día específico
		logger.info(f"Retrive date: {current_date} {type(current_date)}")
		current_data_day = current_data[current_data.index.date == current_date.date()]
		if len(current_data_day) == 0:
			logger.info(f"Skipping {current_date}, shape: {current_data_day.shape}")
			continue
	'''
	for week_num in range(52):
		# Filtrar los datos actuales para el día específico
		print(f"Get datas from {week_num}")
		#current_data_day = current_data[current_data.index.date == current_date.date()]
		current_data_day = current_data[current_data['week']== week_num].drop(columns=['week'])
		if len(current_data_day) == 0:
			print(f"Skipping {week_num}")
			continue
			
		# Configurar el reporte de Evidently
		column_mapping = ColumnMapping(
			prediction=prediction,
			numerical_features=categorical_feats,
			categorical_features=numerical_feats,
			target=target
		)

		# Definir las métricas que queremos calcular
		report = Report(metrics=[
			ColumnDriftMetric(column_name=prediction),
			DatasetDriftMetric(),
			DatasetMissingValuesMetric(),
			RegressionQualityMetric()
		])

		# Calcular las métricas de drift
		report.run(
			reference_data=reference_data, 
			current_data=current_data_day, 
			column_mapping=column_mapping
		)
		result = report.as_dict()

		# Extraer las métricas
		prediction_drift = result['metrics'][0]['result']['drift_score']
		num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
		share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

		# Métricas de RegressionQualityMetric
		r2_score_reference = result['metrics'][3]['result']['reference']['r2_score']
		r2_score_current = result['metrics'][3]['result']['current']['r2_score']

		rmse_score_reference = result['metrics'][3]['result']['reference']['rmse']
		rmse_score_current = result['metrics'][3]['result']['current']['rmse']

		mae_score_reference = result['metrics'][3]['result']['reference']['mean_abs_error']
		mae_score_current = result['metrics'][3]['result']['current']['mean_abs_error']

		mean_error_reference = result['metrics'][3]['result']['reference']['mean_error']
		mean_error_current = result['metrics'][3]['result']['current']['mean_error']

		abs_error_max_reference = result['metrics'][3]['result']['reference']['abs_error_max']
		abs_error_max_current = result['metrics'][3]['result']['current']['abs_error_max']

		mean_abs_perc_error_reference = result['metrics'][3]['result']['reference']['mean_abs_perc_error']
		mean_abs_perc_error_current = result['metrics'][3]['result']['current']['mean_abs_perc_error']

		underperformance_mean_error = result['metrics'][3]['result']['reference']['underperformance']['majority']['mean_error']
		underperformance_std_error = result['metrics'][3]['result']['reference']['underperformance']['majority']['std_error']

		underestimation_mean_error = result['metrics'][3]['result']['reference']['underperformance']['underestimation']['mean_error']
		underestimation_std_error = result['metrics'][3]['result']['reference']['underperformance']['underestimation']['std_error']

		overestimation_mean_error = result['metrics'][3]['result']['reference']['underperformance']['overestimation']['mean_error']
		overestimation_std_error = result['metrics'][3]['result']['reference']['underperformance']['overestimation']['std_error']

		error_std_reference = result['metrics'][3]['result']['reference']['error_std']
		error_std_current = result['metrics'][3]['result']['current']['error_std']

		abs_error_std_reference = result['metrics'][3]['result']['reference']['abs_error_std']
		abs_error_std_current = result['metrics'][3]['result']['current']['abs_error_std']

		abs_perc_error_std_reference = result['metrics'][3]['result']['reference']['abs_perc_error_std']
		abs_perc_error_std_current = result['metrics'][3]['result']['current']['abs_perc_error_std']

		# Incluir el timestamp de este día
		current_date = current_data_day.index[-1].date()
		metrics = {
			'timestamp': current_date,
			'prediction_drift': prediction_drift,
			'num_drifted_columns': num_drifted_columns,
			'share_missing_values': share_missing_values,
			'r2_score_reference':r2_score_reference,
			'r2_score_current': r2_score_current,
			'rmse_score_reference': rmse_score_reference,
			'rmse_score_current': rmse_score_current,
			'mae_score_reference': mae_score_reference,
			'mae_score_current': mae_score_current,
			'mean_error_reference': mean_error_reference,
			'mean_error_current': mean_error_current,
			'abs_error_max_reference': abs_error_max_reference,
			'abs_error_max_current': abs_error_max_current,
			'mean_abs_perc_error_reference': mean_abs_perc_error_reference,
			'mean_abs_perc_error_current': mean_abs_perc_error_current,
			'underperformance_mean_error': underperformance_mean_error,
			'underperformance_std_error': underperformance_std_error,
			'underestimation_mean_error': underestimation_mean_error,
			'underestimation_std_error': underestimation_std_error,
			'overestimation_mean_error': overestimation_mean_error,
			'overestimation_std_error': overestimation_std_error,
			'error_std_reference': error_std_reference,
			'error_std_current': error_std_current,
			'abs_error_std_reference': abs_error_std_reference,
			'abs_error_std_current': abs_error_std_current,
			'abs_perc_error_std_reference': abs_perc_error_std_reference,
			'abs_perc_error_std_current': abs_perc_error_std_current,
		}
		metric_list.append(metrics)

	return pd.DataFrame(metric_list)


@step(
	enable_cache=False
)
def save_metrics_to_db_step(
	host: str,
	port: int,
	database: str,
    metrics: pd.DataFrame #metrics: dict
):
	"""
	Este paso guarda las métricas de drift en la tabla 'citibike_metrics' de PostgreSQL usando SQLAlchemy.
	"""
	# Configuración de SQLAlchemy
	secret = Client().get_secret("pg_monitoring_secret")
	DATABASE_URL = f'postgresql://{secret.secret_values["MONITORING_DB_USER"]}:{secret.secret_values["MONITORING_BD_PASSWORD"]}@{host}:{port}/{database}'
	engine = create_engine(DATABASE_URL)
	Session = sessionmaker(bind=engine)
	
	# Usar el contexto 'with' para manejar la sesión automáticamente
	with Session() as session:
		# Iterar sobre las filas del DataFrame e insertarlas una por una
		for _, row in metrics.iterrows():
			# Crear una nueva instancia de CitibikeMetrics para cada fila del DataFrame
			citibike_metric = CitibikeMetrics(
				timestamp=row['timestamp'],
				prediction_drift=row['prediction_drift'],
				num_drifted_columns=row['num_drifted_columns'],
				share_missing_values=row['share_missing_values'],
				r2_score_reference=row['r2_score_reference'],
				r2_score_current=row['r2_score_current'],
				rmse_score_reference=row['rmse_score_reference'],
				rmse_score_current=row['rmse_score_current'],
				mae_score_reference=row['mae_score_reference'],
				mae_score_current=row['mae_score_current'],
				mean_error_reference=row['mean_error_reference'],
				mean_error_current=row['mean_error_current'],
				abs_error_max_reference=row['abs_error_max_reference'],
				abs_error_max_current=row['abs_error_max_current'],
				mean_abs_perc_error_reference=row['mean_abs_perc_error_reference'],
				mean_abs_perc_error_current=row['mean_abs_perc_error_current'],
				underperformance_mean_error=row['underperformance_mean_error'],
				underperformance_std_error=row['underperformance_std_error'],
				underestimation_mean_error=row['underestimation_mean_error'],
				underestimation_std_error=row['underestimation_std_error'],
				overestimation_mean_error=row['overestimation_mean_error'],
				overestimation_std_error=row['overestimation_std_error'],
				error_std_reference=row['error_std_reference'],
				error_std_current=row['error_std_current'],
				abs_error_std_reference=row['abs_error_std_reference'],
				abs_error_std_current=row['abs_error_std_current'],
				abs_perc_error_std_reference=row['abs_perc_error_std_reference'],
				abs_perc_error_std_current=row['abs_perc_error_std_current'],
			)
			# Insertar la nueva fila en la base de datos
			session.add(citibike_metric)

			logger.info(f"Metrics for {row['timestamp']} saves in table 'citibike_metrics'.")
		# Commit para guardar todos los cambios
		session.commit()
	
	logger.info(f"End save tabla 'citibike_metrics'.")


@pipeline
def batch_monitoring_backfill(
    data_url: str,
    model_name: str,
    model_alias: str,
	host: str,
	port: int,
	database: str,
	start_reference_date: str, 
	end_reference_date: str, 
	start_current_date: str,
	end_current_date: str
):
	logger.info("Starting monitoring")
	logger.info(f"data_url: {data_url}, model_name: {model_name}, model_alias: {model_alias}")	
	logger.info(f"start_reference_date: {start_reference_date}, end_reference_date: {end_reference_date}")
	logger.info(f"start_current_date: {start_current_date}, end_current_date: {end_current_date}")
	start_reference_date = datetime.strptime(start_reference_date, "%Y-%m-%d")
	end_reference_date = datetime.strptime(end_reference_date, "%Y-%m-%d")
	start_current_date = datetime.strptime(start_current_date, "%Y-%m-%d")
	end_current_date = datetime.strptime(end_current_date, "%Y-%m-%d")

	
	# Read 
	create_table_step(
		host=host,
		port=port,
		database=database
	)

	
	# Get model
	model = get_model_by_alias(
		model_name=model_name, 
		model_alias=model_alias,
		after=["create_table_step"]
	)

    
	# Retrieve 
	reference_data, comparison_data, target_col = reference_data_loader(
		base_url=data_url,
		start_reference_date=start_reference_date, 
		end_reference_date=end_reference_date,
		start_current_date=start_current_date, 
		end_current_date=end_current_date,
		after=["get_model_by_alias"]
	)

	# Clean
	reference_data = data_preprocessor(reference_data, is_reference=True)
	comparison_data = data_preprocessor(comparison_data, is_reference=True)

	# Inference
	reference_data, _ = inference_predict(
		model=model,
		dataset_inf=reference_data, 
		categorical_feats=DATASET_CATEGORICAL_COLUMNS,
		numerical_feats=DATASET_NUMERICAL_COLUMNS, 
	)
	comparison_data, prediction_col = inference_predict(
		model=model,
		dataset_inf=comparison_data, 
		categorical_feats=DATASET_CATEGORICAL_COLUMNS,
		numerical_feats=DATASET_NUMERICAL_COLUMNS, 
	)

	json_report, html_report = citibike_data_drift_report(
        reference_dataset=reference_data,
        comparison_dataset=comparison_data,
    )
    
	# Range
	metrics = calculate_drift_metrics_step(
		reference_data=reference_data, 
		current_data=comparison_data, 
		target=target_col, 
		prediction=prediction_col,
		categorical_feats=DATASET_CATEGORICAL_COLUMNS,
		numerical_feats=DATASET_NUMERICAL_COLUMNS, 
	)

	save_metrics_to_db_step(
		host=host,
		port=port,
		database=database,
		metrics=metrics
	)

	logger.info("End monitoring")

#if __name__ == '__main__':
#	batch_monitoring_backfill()