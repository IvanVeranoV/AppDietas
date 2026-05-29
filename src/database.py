import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Configure logger
logger = logging.getLogger("app.database")

class MissingDatabaseConfigurationError(EnvironmentError):
    """
    Exception raised when required database environment variables are missing.
    """
    pass

# Retrieve environment variables strictly (no defaults)

# Cargar las variables desde el archivo .env
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Check for missing variables
missing_vars = []
if not db_user: missing_vars.append("DB_USER")
if not db_password: missing_vars.append("DB_PASSWORD")
if not db_host: missing_vars.append("DB_HOST")
if not db_port: missing_vars.append("DB_PORT")
if not db_name: missing_vars.append("DB_NAME")

if missing_vars:
    error_msg = f"Missing required database configuration: {', '.join(missing_vars)}"
    logger.critical(error_msg)
    raise MissingDatabaseConfigurationError(error_msg)

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    engine = create_engine(database_url, pool_pre_ping=True)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.critical("Failed to initialize database engine with URL", exc_info=True)
    raise

Base = declarative_base()

def get_db():
    """
    FastAPI dependency yielding a database session.
    Directly manages session closure via try...finally to avoid conflict with FastAPI.
    """
    session = session_local()
    try:
        yield session
    except Exception as e:
        logger.error("Exception occurred during database session execution", exc_info=True)
        raise
    finally:
        session.close()
