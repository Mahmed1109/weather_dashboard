from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.routers import weather

load_dotenv()

app = FastAPI(title="Weather Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "Weather Dashboard API is running"}