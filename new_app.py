import requests
from datetime import datetime
import geocoder
import calendar
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk

# Paste you API key from https://weatherapi.com/ here:
api_key = ""

# info for precipitation:
# - Light rain gives up to 2–4 mm (0.07–0.15 in)
# - Moderate rain gives 5–6 mm (0.19–0.23 in)
# - Rain or strong rain gives up about 15–20 mm (0.59–0.78 in)
# - Rainfall gives more than 30 mm (1.18 in)


def format_date(date):
    """ Format date to weekday, day month_name (Monday, 14 May) """
    date_object = datetime.strptime(date, "%Y-%m-%d")
    week_day = calendar.day_name[date_object.weekday()]
    month = date_object.month
    month_name = calendar.month_name[month]
    return f"{week_day[:3]}, {date_object.day} {month_name}"


# root = Tk()
# root.title("World Weather by paichiwo")
# root.geometry("900x500+300+200")
# root.resizable(False, False)
#
# # Search Box
# search_image =
#
# root.mainloop()

user_input = input("Enter location or press (l) for your location: ")
if user_input == "l":
    geo = geocoder.ip('me')
    location = f"{geo.latlng[0]}, {geo.latlng[1]}"
else:
    location = user_input


url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=5&aqi=no&alerts=no"
response = requests.get(url)
data = response.json()

# Info data
city = data['location']['name']
region = data['location']['region']
country = data['location']['country']
local_time = format_date(data['location']['localtime'][:-6])

# Current data
current_temp = data['current']['temp_c']
current_condition = data['current']['condition']['text']
current_feelslike = data['current']['feelslike_c']
current_wind_speed = data['current']['wind_kph']
current_humidity = data['current']['humidity']
current_precipitation = data['current']['precip_mm']  # mm, instead of chance of rain %
current_pressure = data['current']['pressure_mb']
current_is_day = data['current']['is_day']

# Forecast data
forecast = data['forecast']['forecastday']
forecast_data = []

for date_entry in forecast:
    forecast_date = format_date(date_entry['date'])
    forecast_avg_temp = date_entry['day']['avgtemp_c']
    forecast_max_wind = date_entry['day']['maxwind_kph']
    forecast_avg_humidity = date_entry['day']['avghumidity']
    forecast_condition = date_entry['day']['condition']['text']

    forecast_data.append({
        "date": forecast_date,
        "avg_temp": forecast_avg_temp,
        "max_wind": forecast_max_wind,
        "avg_humidity": forecast_avg_humidity,
        "condition": forecast_condition,
    })
