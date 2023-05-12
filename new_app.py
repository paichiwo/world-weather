import requests
from datetime import datetime
import geocoder


def format_date(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    return date_object.strftime("%d/%m/%y")


user_input = input("Enter location or press (l) for your location: ")
if user_input == "l":
    geo = geocoder.ip('me')
    location = f"{geo.latlng[0]}, {geo.latlng[1]}"
else:
    location = input

api_key = "58426b1c8989446e9b7142031230103"
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=5&aqi=no&alerts=no"

# can be post-code, location name(, optional county, country)
# ip address, any language
# querystring = {"q": f"{inp}"}

response = requests.get(url)
data = response.json()

all_data = data

# Current data
current_date = format_date(data['current']['last_updated'][:-6])
current_temp = data['current']['temp_c']
current_condition = data['current']['condition']['text']
current_weather_image = data['current']['condition']['icon'][2:]
current_wind_speed = data['current']['wind_kph']
current_wind_direction = data['current']['wind_dir']
current_pressure = data['current']['pressure_mb']
current_humidity = data['current']['humidity']
current_precipitation = data['current']['precip_mm']
current_feelslike = data['current']['feelslike_c']

# Current print
print(current_date)
print(current_temp)
print(current_condition)
print(current_weather_image)
print(current_wind_speed)
print(current_wind_direction)
print(current_pressure)
print(current_humidity)
print(current_precipitation)
print(current_feelslike)

# Forecast data
forecast = data['forecast']['forecastday']
for date_entry in forecast:
    forecast_date = format_date(date_entry['date'])
    forecast_max_temp = date_entry['day']['maxtemp_c']
    forecast_min_temp = date_entry['day']['mintemp_c']
    forecast_avg_temp = date_entry['day']['avgtemp_c']
    forecast_max_wind = date_entry['day']['maxwind_kph']
    forecast_avg_humidity = date_entry['day']['avghumidity']
    forecast_condition = date_entry['day']['condition']['text']
    forecast_icon = date_entry['day']['condition']['icon'][2:]

    print(forecast_date)

    print(forecast_max_temp)
    print(forecast_min_temp)
    print(forecast_avg_temp)
    print(forecast_max_wind)
    print(forecast_avg_humidity)
    print(forecast_condition)
    print(forecast_icon)
