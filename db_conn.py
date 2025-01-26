import logging
import sqlalchemy as db

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_connection():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        sqlalchemy.engine.base.Connection: Active database connection.
    """
    try:
        engine = db.create_engine("postgresql://postgres:12345@localhost:5432/etl_data")
        conn = engine.connect()
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database. Error: {e}")
        raise
