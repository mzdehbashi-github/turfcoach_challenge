from typing import List
import datetime

import requests
from requests.exceptions import RequestException
from result import Result, Ok, Err
from django.conf import settings

from pitch_health.models import WeatherForecast


def _create_weather_forecast_bulk(json_response: dict, city: str) -> List[WeatherForecast]:
    country = json_response['location']['country']
    weather_forecast_bulk: List[WeatherForecast] = []
    for day_data in json_response['forecast']['forecastday']:
        weather_forecast_bulk.append(
            WeatherForecast(
                location=f"{city}/{country}",
                date=datetime.datetime.strptime(day_data["date"], "%Y-%m-%d").date(),
                daily_will_it_rain=bool(day_data["day"]["daily_will_it_rain"]),
            )
        )

    return WeatherForecast.objects.bulk_create(
        weather_forecast_bulk,
        ignore_conflicts=True,
    )


def update_weather_forecast(city: str, days: int) -> Result[List[WeatherForecast], str]:
    try:
        response = requests.get(
            f"{settings.WEATHER_API_BASE_URL}/forecast.json",
            params={
                "q": city,
                "key": settings.WEATHER_API_KEY,
                "days": days,
            }
        )
    except RequestException as request_exception:
        return Err(f"raised unexpected exception {request_exception=}")

    if response.status_code != 200:
        return Err(
            f"The call to weather API was not successful {response.status_code=}, {response.content=}"
        )

    json_response = response.json()
    objects = _create_weather_forecast_bulk(json_response, city)
    return Ok(objects)


def update_weather_forecast_history(
        city: str,
        start_date: datetime.date,
        end_date: datetime.date
) -> Result[List[WeatherForecast], str]:
    try:
        response = requests.get(
            f"{settings.WEATHER_API_BASE_URL}/history.json",
            params={
                "q": city,
                "key": settings.WEATHER_API_KEY,
                "dt": start_date,
                "end_dt": end_date,
            }
        )
    except RequestException as request_exception:
        return Err(f"raised unexpected exception {request_exception=}")

    if response.status_code != 200:
        return Err(
            f"The call to weather API was not successful {response.status_code=}, {response.content=}"
        )

    json_response = response.json()
    objects = _create_weather_forecast_bulk(json_response, city)
    return Ok(objects)
