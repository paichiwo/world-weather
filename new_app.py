import requests
from datetime import datetime

# Wygrzeb resztę potrzebnych do aplikacji danych
# Przypisz do zmiennych


def format_date(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    return date_object.strftime("%d/%m/%y")


inp = input("Enter location:")
api_key = "58426b1c8989446e9b7142031230103"
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={inp}&days=5&aqi=no&alerts=no"

# can be post-code, location name(, optional county, country)
# ip address, any language
# querystring = {"q": f"{inp}"}

response = requests.get(url)
data = response.json()

all_data = data

# Current data
current_temperature = data['current']['temp_c']
current_weather_image = data['current']['condition']['icon'][2:]
current_condition = data['current']['condition']['text']

# Forecast data
forecast = data['forecast']['forecastday']
for date_entry in forecast:
    forecast_date = date_entry['date']
    print(format_date(forecast_date))
