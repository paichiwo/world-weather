import requests
from datetime import datetime
import geocoder

# Paste you API key from https://weatherapi.com/ here:
key = "58426b1c8989446e9b7142031230103"


def format_date(date):
    """ Format date to european format """
    date_object = datetime.strptime(date, "%Y-%m-%d")
    return date_object.strftime("%d/%m/%y")


def get_weather(location, api_key):
    """ Get all needed weather information from API """
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=5&aqi=no&alerts=no"
    response = requests.get(url)
    data = response.json()

    # Info data
    city = data['location']['name']
    region = data['location']['region']
    country = data['location']['country']
    local_time = format_date(data['location']['localtime'][:-6]) + data['location']['localtime'][10:]

    # Current data
    current_is_day = data['current']['is_day']
    current_temp = data['current']['temp_c']
    current_condition = data['current']['condition']['text']
    current_icon = data['current']['condition']['icon'][2:]
    current_wind_speed = data['current']['wind_kph']
    current_wind_direction = data['current']['wind_dir']
    current_pressure = data['current']['pressure_mb']
    current_humidity = data['current']['humidity']
    current_precipitation = data['current']['precip_mm']
    current_feelslike = data['current']['feelslike_c']

    # Forecast data
    forecast = data['forecast']['forecastday']
    forecast_data = []
    for date_entry in forecast:
        forecast_date = format_date(date_entry['date'])
        forecast_avg_temp = date_entry['day']['avgtemp_c']
        forecast_max_wind = date_entry['day']['maxwind_kph']
        forecast_avg_humidity = date_entry['day']['avghumidity']
        forecast_condition = date_entry['day']['condition']['text']
        forecast_icon = date_entry['day']['condition']['icon'][2:]
        forecast_data.append({
            "date": forecast_date,
            "avg_temp": forecast_avg_temp,
            "max_wind": forecast_max_wind,
            "avg_humidity": forecast_avg_humidity,
            "condition": forecast_condition,
            "icon": forecast_icon
        })

    return {
        "info": {
            "city": city,
            "region": region,
            "country": country,
            "local_time": local_time
        },
        "current": {
            "is_day": current_is_day,
            "temp": current_temp,
            "condition": current_condition,
            "icon": current_icon,
            "wind_speed": current_wind_speed,
            "wind_direction": current_wind_direction,
            "pressure": current_pressure,
            "humidity": current_humidity,
            "precipitation": current_precipitation,
            "feelslike": current_feelslike
        },
        "forecast": forecast_data
    }


user_input = input("Enter location or press (l) for your location: ")
if user_input == "l":
    geo = geocoder.ip('me')
    user_location = f"{geo.latlng[0]}, {geo.latlng[1]}"
else:
    user_location = input
print(get_weather(user_location, key))
