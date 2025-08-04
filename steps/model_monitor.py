from typing import Tuple, Annotated, List
import datetime
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
    RegressionQualityMetric,
)
from zenml import step
from zenml.client import Client
from zenml.logger import get_logger

SEND_TIMEOUT = 10

logger = get_logger(__name__)

# Base de datos para los modelos de SQLAlchemy
Base = declarative_base()


def daterange(start_date: datetime.date, end_date: datetime.date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + datetime.timedelta(n)


# Definimos el modelo de la tabla citibike_metrics
class CitibikeMetrics(Base):
    __tablename__ = "citibike_metrics"

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
@step(enable_cache=False)
def create_table_step(host: str, port: int, database: str):
    """
    Este paso asegura que la tabla 'citibike_metrics' exista en la base de datos.
    """
    # Configuración de SQLAlchemy
    secret = Client().get_secret("pg_monitoring_secret")
    DATABASE_URL = f'postgresql://{secret.secret_values["MONITORING_DB_USER"]}:{secret.secret_values["MONITORING_BD_PASSWORD"]}@{host}:{port}/{database}'

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    logger.info("Tabla 'citibike_metrics' verificada o creada exitosamente.")


@step(enable_cache=False)
def calculate_drift_metrics_step(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    target: str,
    prediction: str,
    categorical_feats: List[str] = [],
    numerical_feats: List[str] = [],
) -> Annotated[pd.DataFrame, "metrics"]:
    """
    Este paso calcula las métricas de drift usando Evidently (model drift, column drift, missing values).
    """
    # Calculate predictions
    logger.info("Calculate predictions")
    feats = categorical_feats + numerical_feats
    feats = feats if len(feats) else reference_data.columns
    current_data["week"] = current_data.index.isocalendar().week

    metric_list = []
    for week_num in range(52):
        # Filtrar los datos actuales para el día específico
        print(f"Get datas from {week_num}")
        # current_data_day = current_data[current_data.index.date == current_date.date()]
        current_data_day = current_data[current_data["week"] == week_num].drop(
            columns=["week"]
        )
        if len(current_data_day) == 0:
            print(f"Skipping {week_num}")
            continue

        # Configurar el reporte de Evidently
        column_mapping = ColumnMapping(
            prediction=prediction,
            numerical_features=categorical_feats,
            categorical_features=numerical_feats,
            target=target,
        )

        # Definir las métricas que queremos calcular
        report = Report(
            metrics=[
                ColumnDriftMetric(column_name=prediction),
                DatasetDriftMetric(),
                DatasetMissingValuesMetric(),
                RegressionQualityMetric(),
            ]
        )

        # Calcular las métricas de drift
        report.run(
            reference_data=reference_data,
            current_data=current_data_day,
            column_mapping=column_mapping,
        )
        result = report.as_dict()

        # Extraer las métricas
        prediction_drift = result["metrics"][0]["result"]["drift_score"]
        num_drifted_columns = result["metrics"][1]["result"][
            "number_of_drifted_columns"
        ]
        share_missing_values = result["metrics"][2]["result"]["current"][
            "share_of_missing_values"
        ]

        # Métricas de RegressionQualityMetric
        r2_score_reference = result["metrics"][3]["result"]["reference"][
            "r2_score"
        ]
        r2_score_current = result["metrics"][3]["result"]["current"][
            "r2_score"
        ]

        rmse_score_reference = result["metrics"][3]["result"]["reference"][
            "rmse"
        ]
        rmse_score_current = result["metrics"][3]["result"]["current"]["rmse"]

        mae_score_reference = result["metrics"][3]["result"]["reference"][
            "mean_abs_error"
        ]
        mae_score_current = result["metrics"][3]["result"]["current"][
            "mean_abs_error"
        ]

        mean_error_reference = result["metrics"][3]["result"]["reference"][
            "mean_error"
        ]
        mean_error_current = result["metrics"][3]["result"]["current"][
            "mean_error"
        ]

        abs_error_max_reference = result["metrics"][3]["result"]["reference"][
            "abs_error_max"
        ]
        abs_error_max_current = result["metrics"][3]["result"]["current"][
            "abs_error_max"
        ]

        mean_abs_perc_error_reference = result["metrics"][3]["result"][
            "reference"
        ]["mean_abs_perc_error"]
        mean_abs_perc_error_current = result["metrics"][3]["result"][
            "current"
        ]["mean_abs_perc_error"]

        underperformance_mean_error = result["metrics"][3]["result"][
            "reference"
        ]["underperformance"]["majority"]["mean_error"]
        underperformance_std_error = result["metrics"][3]["result"][
            "reference"
        ]["underperformance"]["majority"]["std_error"]

        underestimation_mean_error = result["metrics"][3]["result"][
            "reference"
        ]["underperformance"]["underestimation"]["mean_error"]
        underestimation_std_error = result["metrics"][3]["result"][
            "reference"
        ]["underperformance"]["underestimation"]["std_error"]

        overestimation_mean_error = result["metrics"][3]["result"][
            "reference"
        ]["underperformance"]["overestimation"]["mean_error"]
        overestimation_std_error = result["metrics"][3]["result"]["reference"][
            "underperformance"
        ]["overestimation"]["std_error"]

        error_std_reference = result["metrics"][3]["result"]["reference"][
            "error_std"
        ]
        error_std_current = result["metrics"][3]["result"]["current"][
            "error_std"
        ]

        abs_error_std_reference = result["metrics"][3]["result"]["reference"][
            "abs_error_std"
        ]
        abs_error_std_current = result["metrics"][3]["result"]["current"][
            "abs_error_std"
        ]

        abs_perc_error_std_reference = result["metrics"][3]["result"][
            "reference"
        ]["abs_perc_error_std"]
        abs_perc_error_std_current = result["metrics"][3]["result"]["current"][
            "abs_perc_error_std"
        ]

        # Incluir el timestamp de este día
        current_date = current_data_day.index[-1].date()
        metrics = {
            "timestamp": current_date,
            "prediction_drift": prediction_drift,
            "num_drifted_columns": num_drifted_columns,
            "share_missing_values": share_missing_values,
            "r2_score_reference": r2_score_reference,
            "r2_score_current": r2_score_current,
            "rmse_score_reference": rmse_score_reference,
            "rmse_score_current": rmse_score_current,
            "mae_score_reference": mae_score_reference,
            "mae_score_current": mae_score_current,
            "mean_error_reference": mean_error_reference,
            "mean_error_current": mean_error_current,
            "abs_error_max_reference": abs_error_max_reference,
            "abs_error_max_current": abs_error_max_current,
            "mean_abs_perc_error_reference": mean_abs_perc_error_reference,
            "mean_abs_perc_error_current": mean_abs_perc_error_current,
            "underperformance_mean_error": underperformance_mean_error,
            "underperformance_std_error": underperformance_std_error,
            "underestimation_mean_error": underestimation_mean_error,
            "underestimation_std_error": underestimation_std_error,
            "overestimation_mean_error": overestimation_mean_error,
            "overestimation_std_error": overestimation_std_error,
            "error_std_reference": error_std_reference,
            "error_std_current": error_std_current,
            "abs_error_std_reference": abs_error_std_reference,
            "abs_error_std_current": abs_error_std_current,
            "abs_perc_error_std_reference": abs_perc_error_std_reference,
            "abs_perc_error_std_current": abs_perc_error_std_current,
        }
        metric_list.append(metrics)

    return pd.DataFrame(metric_list)


@step(enable_cache=False)
def save_metrics_to_db_step(
    host: str, port: int, database: str, metrics: pd.DataFrame  # metrics: dict
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
                timestamp=row["timestamp"],
                prediction_drift=row["prediction_drift"],
                num_drifted_columns=row["num_drifted_columns"],
                share_missing_values=row["share_missing_values"],
                r2_score_reference=row["r2_score_reference"],
                r2_score_current=row["r2_score_current"],
                rmse_score_reference=row["rmse_score_reference"],
                rmse_score_current=row["rmse_score_current"],
                mae_score_reference=row["mae_score_reference"],
                mae_score_current=row["mae_score_current"],
                mean_error_reference=row["mean_error_reference"],
                mean_error_current=row["mean_error_current"],
                abs_error_max_reference=row["abs_error_max_reference"],
                abs_error_max_current=row["abs_error_max_current"],
                mean_abs_perc_error_reference=row[
                    "mean_abs_perc_error_reference"
                ],
                mean_abs_perc_error_current=row["mean_abs_perc_error_current"],
                underperformance_mean_error=row["underperformance_mean_error"],
                underperformance_std_error=row["underperformance_std_error"],
                underestimation_mean_error=row["underestimation_mean_error"],
                underestimation_std_error=row["underestimation_std_error"],
                overestimation_mean_error=row["overestimation_mean_error"],
                overestimation_std_error=row["overestimation_std_error"],
                error_std_reference=row["error_std_reference"],
                error_std_current=row["error_std_current"],
                abs_error_std_reference=row["abs_error_std_reference"],
                abs_error_std_current=row["abs_error_std_current"],
                abs_perc_error_std_reference=row[
                    "abs_perc_error_std_reference"
                ],
                abs_perc_error_std_current=row["abs_perc_error_std_current"],
            )
            # Insertar la nueva fila en la base de datos
            session.add(citibike_metric)

            logger.info(
                f"Metrics for {row['timestamp']} saves in table 'citibike_metrics'."
            )
        # Commit para guardar todos los cambios
        session.commit()

    logger.info("End save tabla 'citibike_metrics'.")
