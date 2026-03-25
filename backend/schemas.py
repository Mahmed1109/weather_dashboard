from pydantic import BaseModel
from typing import Optional

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