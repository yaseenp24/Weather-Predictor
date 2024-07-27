import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from geocoding import Geocoding

class Weather:
    BASE_URL_REVERSE = Geocoding.BASE_URL_REVERSE
    BASE_WEATHER_URL = 'https://api.weather.gov/points/'

    @staticmethod
    def build_search_url(lat: float, lon: float) -> dict:
        search_url = f'{Weather.BASE_WEATHER_URL}{lat},{lon}'
        result = Geocoding.get_result(search_url)

        forecast_hourly_link = result.get('properties', {}).get('forecastHourly')
        if forecast_hourly_link:
            forecast_hourly_link = Geocoding.get_result(forecast_hourly_link)
            return forecast_hourly_link

    @staticmethod
    def extreme_temp(api_response: dict, hours: int, limit: str, scale: str) -> None:
        periods = api_response.get('properties', {}).get('periods', [])

        if not periods:
            print("No hourly forecast data found.")
            return

        extreme_temperature = float('-inf') if limit == "MAX" else float('inf')
        extreme_temperature_time = None

        for period in periods[:hours]:
            temperature = period.get('temperature', 0)

            if (limit == "MAX" and temperature > extreme_temperature) or (limit == "MIN" and temperature < extreme_temperature):
                extreme_temperature = temperature
                extreme_temperature_time = period.get('startTime')
                start_datetime = datetime.strptime(extreme_temperature_time, "%Y-%m-%dT%H:%M:%S%z")
                formatted_start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        if scale.lower() == 'f':
            return (formatted_start_time, extreme_temperature)
        elif scale.lower() == 'c':
            celsius_temperature = (extreme_temperature - 32) * 5.0/9.0
            return (formatted_start_time, celsius_temperature)

    @staticmethod
    def temp_feels(api_response: dict, hours: int, limit: str, scale: str):
        t = Weather.extreme_temp(api_response, hours, limit, scale)
        h = Weather.extreme_humidity(api_response, hours, limit)
        w = Weather.extreme_wind(api_response, hours, limit)
        if t[1] >= 68:
            heat_index = (-42.379) + (2.04901523 * t[1]) + (10.14333127 * h[1]) + (-0.22475541 * t[1] * h[1]) + (-0.00683783 * t[1] * t[1]) + (-0.05481717 * h[1] * h[1]) + (0.00122847 * t[1] * t[1] * h[1]) + (0.00085282 * t[1] * h[1] * h[1]) + (-0.00000199 * t[1] * t[1] * h[1] * h[1])
            return t[0], heat_index
        if t[1] <= 50 and w[1] > 3:
            wind_chill = (35.74) + (0.6215 * t[1]) + (-35.75 * (w[1]**0.16)) + (0.4275 * t[1] * (w[1]**0.16))
            return w[0], wind_chill
        else:
            air_temp = t[1]
            return t[0], air_temp

    @staticmethod
    def extreme_humidity(api_response: dict, hours: int, limit: str) -> None:
        periods = api_response.get('properties', {}).get('periods', [])

        if not periods:
            print("No hourly forecast data found.")
            return

        extreme_humidity_percent = float('-inf') if limit == "MAX" else float('inf')
        extreme_humidity_time = None

        for period in periods[:hours]:
            humidity_data = period.get('relativeHumidity', {})

            if isinstance(humidity_data, dict):
                # Handle the case where 'relativeHumidity' is a dictionary
                humidity_percent = humidity_data.get('value', 0)
            else:
                humidity_percent = humidity_data

            if (limit == "MAX" and humidity_percent > extreme_humidity_percent) or (limit == "MIN" and humidity_percent < extreme_humidity_percent):
                extreme_humidity_percent = humidity_percent
                extreme_humidity_time = period.get('startTime')
                start_datetime = datetime.strptime(extreme_humidity_time, "%Y-%m-%dT%H:%M:%S%z")
                formatted_start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        return (formatted_start_time, extreme_humidity_percent)

    @staticmethod
    def extreme_wind(api_response: dict, hours: int, limit: str) -> str:
        periods = api_response.get('properties', {}).get('periods', [])

        if not periods:
            return "No hourly forecast data found."

        extreme_wind_speed = float('-inf') if limit == "MAX" else float('inf')
        extreme_wind_time = None

        for period in periods[:hours]:
            wind_speed = float(period.get('windSpeed', '0').split(' ')[0])

            if (limit == "MAX" and wind_speed > extreme_wind_speed) or (limit == "MIN" and wind_speed < extreme_wind_speed):
                extreme_wind_speed = wind_speed
                extreme_wind_time = period.get('startTime')
                start_datetime = datetime.strptime(extreme_wind_time, "%Y-%m-%dT%H:%M:%S%z")
                formatted_start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        return (formatted_start_time, extreme_wind_speed)

    @staticmethod
    def extreme_precipitation(api_response: dict, hours: int, limit: str) -> None:
        periods = api_response.get('properties', {}).get('periods', [])

        if not periods:
            print("No hourly forecast data found.")
            return

        extreme_precipitation_chance = float('-inf') if limit == "MAX" else float('inf')
        extreme_precipitation_time = None

        for period in periods[:hours]:
            precipitation_data = period.get('probabilityOfPrecipitation', {})

            if isinstance(precipitation_data, dict):
                # Handle the case where 'probabilityOfPrecipitation' is a dictionary
                precipitation_chance = precipitation_data.get('value', 0)
            else:
                precipitation_chance = precipitation_data

            if (limit == "MAX" and precipitation_chance > extreme_precipitation_chance) or (limit == "MIN" and precipitation_chance < extreme_precipitation_chance):
                extreme_precipitation_chance = precipitation_chance
                extreme_precipitation_time = period.get('startTime')
                start_datetime = datetime.strptime(extreme_precipitation_time, "%Y-%m-%dT%H:%M:%S%z")
                formatted_start_time = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        return (formatted_start_time, extreme_precipitation_chance)
