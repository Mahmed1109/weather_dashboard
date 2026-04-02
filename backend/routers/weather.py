from fastapi import APIRouter, HTTPException, Query
import httpx
import os
from dotenv import load_dotenv
from backend.schemas import WeatherResponse, ForecastResponse, ForecastItem

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

router = APIRouter(prefix="/weather", tags=["weather"])

def parse_weather(data: dict, units: str = "metric") -> WeatherResponse:
    return WeatherResponse(
        city=data["name"],
        country=data["sys"]["country"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        temp_min=data["main"]["temp_min"],
        temp_max=data["main"]["temp_max"],
        humidity=data["main"]["humidity"],
        pressure=data["main"]["pressure"],
        wind_speed=data["wind"]["speed"],
        description=data["weather"][0]["description"],
        icon=data["weather"][0]["icon"],
        visibility=data["visibility"],
        units=units
    )

async def fetch_weather(city: str, units: str = "metric") -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": units
            }
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found. Please check the spelling and try again.")
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching weather data")

    return response.json()

@router.get("/current/{city}", response_model=WeatherResponse)
async def get_weather(
    city: str,
    units: str = Query("metric", description="Units: metric or imperial")
):
    data = await fetch_weather(city, units)
    return parse_weather(data, units)

@router.get("/search", response_model=WeatherResponse)
async def search_weather(
    q: str = Query(..., description="City name to search"),
    units: str = Query("metric", description="Units: metric or imperial")
):
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    data = await fetch_weather(q.strip(), units)
    return parse_weather(data, units)

@router.get("/forecast/{city}", response_model=ForecastResponse)
async def get_forecast(
    city: str,
    units: str = Query("metric", description="Units: metric or imperial")
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/forecast",
            params={
                "q": city,
                "appid": API_KEY,
                "units": units
            }
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching forecast data")

    data = response.json()

    forecast_items = []
    for item in data["list"]:
        dt_parts = item["dt_txt"].split(" ")
        forecast_items.append(ForecastItem(
            date=dt_parts[0],
            time=dt_parts[1],
            temperature=item["main"]["temp"],
            feels_like=item["main"]["feels_like"],
            description=item["weather"][0]["description"],
            icon=item["weather"][0]["icon"],
            humidity=item["main"]["humidity"],
            wind_speed=item["wind"]["speed"]
        ))

    return ForecastResponse(
        city=data["city"]["name"],
        country=data["city"]["country"],
        forecast=forecast_items,
        units=units
    )