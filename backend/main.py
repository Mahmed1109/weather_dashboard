from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
from backend.schemas import WeatherResponse

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

app = FastAPI(title="Weather Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Weather Dashboard API is running"}

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key")

    data = response.json()

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
        visibility=data["visibility"]
    )