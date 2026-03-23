from fastapi import FastAPI

app = FastAPI(title="Weather Dashboard", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Weather Dashboard API is running"}