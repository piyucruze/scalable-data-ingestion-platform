CREATE TABLE IF NOT EXISTS market_data (
    instrument_id VARCHAR(20) NOT NULL,
    price NUMERIC(18,2) NOT NULL,
    volume NUMERIC(18,2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    vwap NUMERIC(18,2) NOT NULL,
    is_outlier BOOLEAN NOT NULL,
    PRIMARY KEY (instrument_id, timestamp)
);