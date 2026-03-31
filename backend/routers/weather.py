from fastapi import APIRouter, HTTPException, Query
import httpx
import os
from backend.schemas import WeatherResponse, ForecastResponse, ForecastItem

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

router = APIRouter(prefix="/weather", tags=["weather"])