



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
    