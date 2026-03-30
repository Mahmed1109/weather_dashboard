from pydantic import BaseModel
from typing import List, Optional

class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    wind_speed: float
    description: str
    icon: str
    visibility: int
    units: str = "metric"

class ForecastItem(BaseModel):
    date: str
    time: str
    temperature: float
    feels_like: float
    description: str
    icon: str
    humidity: int
    wind_speed: float

class ForecastResponse(BaseModel):
    city: str
    country: str
    forecast: List[ForecastItem]
    units: str = "metric"

class ErrorResponse(BaseModel):
    detail: str
    city: Optional[str] = None