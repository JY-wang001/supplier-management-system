import requests
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.supplier import WeatherData
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Shanghai")


def get_weather_data(date_str: str = None):
    if not WEATHER_API_KEY:
        return None

    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "date": date.today(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "precipitation": data.get("rain", {}).get("1h", 0),
                "wind_speed": data["wind"]["speed"],
                "weather_condition": data["weather"][0]["main"],
                "city": WEATHER_CITY
            }
        else:
            return None
    except Exception as e:
        return None


def save_weather_data(db: Session, weather_info: dict):
    existing = db.query(WeatherData).filter(
        WeatherData.date == weather_info["date"]
    ).first()

    if existing:
        existing.temperature = weather_info["temperature"]
        existing.humidity = weather_info["humidity"]
        existing.precipitation = weather_info["precipitation"]
        existing.wind_speed = weather_info["wind_speed"]
        existing.weather_condition = weather_info["weather_condition"]
        existing.city = weather_info["city"]
    else:
        weather = WeatherData(**weather_info)
        db.add(weather)

    db.commit()
    return weather_info


def get_historical_weather(db: Session, start_date: date, end_date: date):
    return db.query(WeatherData).filter(
        WeatherData.date >= start_date,
        WeatherData.date <= end_date
    ).all()