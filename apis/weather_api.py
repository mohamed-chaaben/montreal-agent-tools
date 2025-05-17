import aiohttp
from datetime import datetime
from fastapi import HTTPException


WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

async def get_weather():
  """
  Returns the current weather and the current time.
  """
  params = {
      "latitude": 45.5017,
      "longitude": -73.5673,
      "current":
      "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
      "timezone": "America/New_York",
      "forecast_days": 1
  }
  try:
      async with aiohttp.ClientSession() as session:
          async with session.get(WEATHER_API_URL, params=params) as response:
              if response.status != 200:
                  raise HTTPException(status_code=response.status,
                                      detail="Failed to fetch weather data")

              data = await response.json()
              current = data["current"]

              weather_codes = {
                  0: "Clear sky",
                  1: "Mainly clear",
                  2: "Partly cloudy",
                  3: "Overcast",
                  45: "Foggy",
                  48: "Depositing rime fog",
                  51: "Light drizzle",
                  53: "Moderate drizzle",
                  55: "Dense drizzle",
                  61: "Slight rain",
                  63: "Moderate rain",
                  65: "Heavy rain",
                  71: "Slight snow",
                  73: "Moderate snow",
                  75: "Heavy snow",
                  77: "Snow grains",
                  80: "Slight rain showers",
                  81: "Moderate rain showers",
                  82: "Violent rain showers",
                  85: "Slight snow showers",
                  86: "Heavy snow showers",
                  95: "Thunderstorm",
                  96: "Thunderstorm with slight hail",
                  99: "Thunderstorm with heavy hail"
              }

              return {
                  "main": {
                      "temp": current["temperature_2m"],
                      "humidity": current["relative_humidity_2m"],
                      "precipitation": current["precipitation"]
                  },
                  "weather": [{
                      "description":
                      weather_codes.get(current["weather_code"], "Unknown"),
                      "code":
                      current["weather_code"]
                  }],
                  "wind": {
                      "speed": current["wind_speed_10m"],
                      "deg": current["wind_direction_10m"]
                  },
                  "dt":
                  datetime.now()
              }
  except Exception as e:
      raise HTTPException(status_code=500,
                          detail=f"Failed to fetch weather data: {str(e)}")
