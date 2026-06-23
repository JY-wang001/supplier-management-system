from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from schemas.supplier import WeatherData as WeatherDataSchema
from services.weather import get_weather_data, save_weather_data, get_historical_weather
from database import get_db

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current")
def fetch_current_weather(db: Session = Depends(get_db)):
    weather_info = get_weather_data()
    if weather_info:
        save_weather_data(db, weather_info)
        return weather_info
    raise HTTPException(status_code=500, detail="Failed to fetch weather data")


@router.get("/historical", response_model=List[WeatherDataSchema])
def fetch_historical_weather(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return get_historical_weather(db, start_date, end_date)