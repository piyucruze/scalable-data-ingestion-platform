import logging
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)


def wait_for_db(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            with engine.connect():
                logging.info("Database connection successful.")
                return
        except Exception:
            logging.warning(
                f"Database not ready. Retrying {attempt + 1}/{max_retries}..."
            )
            time.sleep(delay)

    raise Exception("Database not available after retries.")


def insert_records(records):
    if not records:
        return

    insert_query = """
        INSERT INTO market_data 
        (instrument_id, price, volume, timestamp, vwap, is_outlier)
        VALUES 
        (:instrument_id, :price, :volume, :timestamp, :vwap, :is_outlier)
        ON CONFLICT (instrument_id, timestamp) DO NOTHING
    """

    try:
        with engine.begin() as connection:
            connection.execute(text(insert_query), records)

        logging.info(f"{len(records)} records inserted into DB.")

    except SQLAlchemyError as e:
        logging.error(f"Insert failed: {e}")