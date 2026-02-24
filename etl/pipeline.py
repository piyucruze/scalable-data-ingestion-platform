import requests
import time
import logging
from collections import defaultdict
from datetime import datetime
from pydantic import ValidationError
from models import MarketData
from db import insert_records, wait_for_db

API_URL = "http://api:8000/v1/market-data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_market_data():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API fetch failed: {e}")
        return []


def validate_records(raw_records):
    valid_records = []
    dropped = 0

    for record in raw_records:
        try:
            validated = MarketData(**record)
            valid_records.append(validated)
        except ValidationError:
            dropped += 1

    return valid_records, dropped


def calculate_vwap(records):
    grouped = defaultdict(list)

    for r in records:
        grouped[r.instrument_id].append(r)

    vwap_map = {}

    for instrument, items in grouped.items():
        total_price_volume = sum(r.price * r.volume for r in items)
        total_volume = sum(r.volume for r in items)
        vwap_map[instrument] = total_price_volume / total_volume

    return vwap_map


def detect_outliers(records, vwap_map):
    final_records = []

    for r in records:
        avg_price = vwap_map[r.instrument_id]
        deviation = abs(r.price - avg_price) / avg_price

        is_outlier = deviation > 0.15

        final_records.append({
            "instrument_id": r.instrument_id,
            "price": r.price,
            "volume": r.volume,
            "timestamp": r.timestamp,
	    "vwap": avg_price, 
            "is_outlier": is_outlier
        })

    return final_records


def run_pipeline():
    start_time = time.time()

    raw_data = fetch_market_data()
    if not raw_data:
        return

    valid_records, dropped = validate_records(raw_data)

    if not valid_records:
        logging.warning("All records failed validation.")
        return

    vwap_map = calculate_vwap(valid_records)
    processed_records = detect_outliers(valid_records, vwap_map)

    insert_records(processed_records)

    execution_time = round(time.time() - start_time, 3)

    logging.info(
        f"Processed: {len(valid_records)}, "
        f"Dropped: {dropped}, "
        f"Execution Time: {execution_time}s"
    )


if __name__ == "__main__":
    logging.info("ETL Service Started...")
    
    wait_for_db()  # Only wait for DB, don't create table

    while True:
        try:
            run_pipeline()
            time.sleep(30)
        except Exception as e:
            logging.error(f"Pipeline crashed: {e}")
            time.sleep(10)

