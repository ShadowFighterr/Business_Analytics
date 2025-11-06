"""
Custom API Exporter (Corrected Version)
Example: collecting weather data for Astana (Open-Meteo API)
"""

from prometheus_client import start_http_server, Gauge, Info
import requests
import time

# This was missing in the lecture, but required by the script
exporter_info = Info('custom_exporter', 'Info about the custom exporter')

# Weather metrics (Astana) - 10 total
weather_temperature = Gauge(
    'weather_temperature_celsius',
    'Current temperature in Astana',
    ['city', 'country']
)

weather_windspeed = Gauge(
    'weather_windspeed_kmh',
    'Current wind speed in Astana',
    ['city', 'country']
)

weather_api_status = Gauge(
    'weather_api_status',
    'Weather API status (1=up, 0=down)'
)

weather_humidity = Gauge(
    'weather_humidity_percent',
    'Current relative humidity in Astana',
    ['city', 'country']
)

weather_apparent_temp = Gauge(
    'weather_apparent_temperature_celsius',
    'Current apparent (feels-like) temperature in Astana',
    ['city', 'country']
)

weather_rain = Gauge(
    'weather_rain_mm',
    'Current rain in mm',
    ['city', 'country']
)

weather_showers = Gauge(
    'weather_showers_mm',
    'Current showers in mm',
    ['city', 'country']
)

weather_snowfall = Gauge(
    'weather_snowfall_cm',
    'Current snowfall in cm',
    ['city', 'country']
)

weather_cloudcover = Gauge(
    'weather_cloudcover_percent',
    'Current cloudcover in percent',
    ['city', 'country']
)

weather_wind_direction = Gauge(
    'weather_wind_direction_degrees',
    'Current wind direction in degrees',
    ['city', 'country']
)


def fetch_weather_data():
    """
    Get weather data for Astana via Open-Meteo API
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        
        # We will request all metrics using the 'current' parameter
        all_metrics = "temperature_2m,relative_humidity_2m,apparent_temperature,rain,showers,snowfall,cloud_cover,wind_speed_10m,wind_direction_10m"
        
        params = {
            'latitude': 51.1694,
            'longitude': 71.4491,
            'current': all_metrics,
            'timezone': 'Asia/Almaty'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()

        # Check for API errors returned in the JSON
        if data.get('error'):
            print(f"API Error: {data.get('reason', 'Unknown reason')}")
            weather_api_status.set(0)
            return False

        # This is the key we need. All data is inside this object.
        current = data['current']
        
        # Set all 10 metrics
        weather_temperature.labels(city='Astana', country='Kazakhstan').set(current['temperature_2m'])
        weather_windspeed.labels(city='Astana', country='Kazakhstan').set(current['wind_speed_10m'])
        weather_humidity.labels(city='Astana', country='Kazakhstan').set(current['relative_humidity_2m'])
        weather_apparent_temp.labels(city='Astana', country='Kazakhstan').set(current['apparent_temperature'])
        weather_rain.labels(city='Astana', country='Kazakhstan').set(current['rain'])
        weather_showers.labels(city='Astana', country='Kazakhstan').set(current['showers'])
        weather_snowfall.labels(city='Astana', country='Kazakhstan').set(current['snowfall'])
        weather_cloudcover.labels(city='Astana', country='Kazakhstan').set(current['cloud_cover'])
        weather_wind_direction.labels(city='Astana', country='Kazakhstan').set(current['wind_direction_10m'])
        
        # Set API status to UP
        weather_api_status.set(1)
        print("Weather data updated successfully.")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        weather_api_status.set(0)
        return False
    except KeyError as e:
        print(f"KeyError: Could not find key {e} in API response. Response data: {data}")
        weather_api_status.set(0)
        return False


if __name__ == '__main__':
    exporter_info.info({
        'version': '1.0',
        'author': 'Student',
        'sources': 'open-meteo'
    })
    
    start_http_server(8000)
    print("Custom exporter started on http://localhost:8000")
    
    while True:
        try:
            fetch_weather_data()
        except KeyboardInterrupt:
            print("Exporter stopping...")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the loop: {e}")
        
        # Update every 30 seconds
        time.sleep(30)
