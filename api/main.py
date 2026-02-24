from fastapi import FastAPI, HTTPException
from datetime import datetime
import random
from typing import List
from models import MarketDataResponse

app = FastAPI()

INSTRUMENTS = ["AAPL", "GOOG", "MSFT", "BTC-USD", "ETH-USD"]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/market-data", response_model=List[MarketDataResponse])
def get_market_data():

    # 5% fault injection
    if random.random() < 0.05:
        if random.random() < 0.5:
            raise HTTPException(status_code=500, detail="Injected failure")
        else:
            # malformed data
            return [{
                "instrument_id": "AAPL",
                "price": "INVALID",   # wrong type
                "volume": 100,
                "timestamp": datetime.utcnow()
            }]

    data = []

    for _ in range(20):
        instrument = random.choice(INSTRUMENTS)
        price = round(random.uniform(100, 50000), 2)
        volume = round(random.uniform(1, 1000), 2)

        data.append({
            "instrument_id": instrument,
            "price": price,
            "volume": volume,
            "timestamp": datetime.utcnow()
        })

    return data