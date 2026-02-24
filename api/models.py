from pydantic import BaseModel
from datetime import datetime

class MarketDataResponse(BaseModel):
    instrument_id: str
    price: float
    volume: float
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "instrument_id": "AAPL",
                "price": 4152.68,
                "volume": 356.21,
                "timestamp": "2026-02-23T15:12:33.950418"
            }
        }