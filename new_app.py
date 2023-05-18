from datetime import datetime
from tkinter import *
import tkinter as tk
import requests
import calendar
import json
from weather_icons import icons

# Create the window and set the basics
root = Tk()
root.title('World Weather by paichiwo')
root.geometry('350x680+300+200')
root.resizable(False, False)
root.config(bg='black')

# info for precipitation:
# - Light rain gives up to 2–4 mm (0.07–0.15 in)
# - Moderate rain gives 5–6 mm (0.19–0.23 in)
# - Rain or strong rain gives up about 15–20 mm (0.59–0.78 in)
# - Rainfall gives more than 30 mm (1.18 in)


def format_date(date):
    """ Format date to weekday, day month_name (Monday, 14 May) """
    date_object = datetime.strptime(date, '%Y-%m-%d')
    week_day = calendar.day_name[date_object.weekday()]
    month = date_object.month
    month_name = calendar.month_name[month]
    return f'{week_day[:3]}, {date_object.day} {month_name}'


def country_code(country_name):
    """ Change full country name to its abbreviation """
    with open('country_code.json') as file:
        json_data = json.load(file)
    for name in json_data:
        if name['Name'] == country_name:
            return name['Code']


def get_weather():
    api_key = '58426b1c8989446e9b7142031230103'
    location = textfield.get()
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&aqi=no&alerts=no'
    data = requests.get(url).json()

    # Info data
    city = data['location']['name']
    country = country_code(data['location']['country'])
    local_time = format_date(data['location']['localtime'][:-6])

    # Current data
    code = data['current']['condition']['code']
    current_temp = str(int(data['current']['temp_c']))
    current_condition = data['current']['condition']['text']
    current_feelslike = str(int(data['current']['feelslike_c']))
    current_wind_speed = str(int(data['current']['wind_kph']))
    current_humidity = data['current']['humidity']
    current_precipitation = str(int(data['current']['precip_mm']))  # mm, instead of chance of rain %
    current_pressure = str(int(data['current']['pressure_mb']))
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
            'date': forecast_date,
            'avg_temp': forecast_avg_temp,
            'max_wind': forecast_max_wind,
            'avg_humidity': forecast_avg_humidity,
            'condition': forecast_condition,
        })

    # Update labels with data from the API
    city_info.config(text=f'{city}, {country}', justify='center', width=22)
    weather_icon.config(file=icons[code])
    temp.config(text=current_temp, justify='center', bg=l_blue, fg='white', width=2)
    if len(current_temp) == 1:
        temp_symbol.config(text='°', justify='center', bg=l_blue, fg='white')
        temp_symbol.place(x=206, y=290)
    else:
        temp_symbol.config(text='°', justify='center', bg=l_blue, fg='white')
        temp_symbol.place(x=240, y=290)
    condition.config(text=current_condition, justify='center', bg=l_blue, fg='white')
    date.config(text=local_time, justify='center', bg=l_blue, fg='white')
    feelslike.config(text=f'{current_feelslike}°', justify='center', bg=l_blue, fg='white')
    wind.config(text=f'{current_wind_speed} km/h', justify='center', bg=l_blue, fg='white')
    humidity.config(text=f'{current_humidity}%', justify='center', bg=l_blue, fg='white')
    precipitation.config(text=f'{current_precipitation} mm', justify='center', bg=l_blue, fg='white')
    pressure.config(text=f'{current_pressure} hPa', justify='center', bg=l_blue, fg='white')

# Colors
l_blue = '#1581ef'
d_blue = '#1167f2'

# ------------------- SEARCH BOX ---------------------
# Search box image
Search_image = PhotoImage(file='img/current_window.png')
search_label = Label(image=Search_image, bg='black')
search_label.place(x=22, y=20)

# Input field
textfield = tk.Entry(root, justify='center', width=25, font=('Noto Sans', 11, 'bold'), bg=d_blue, border=0, fg='white')
textfield.place(x=60, y=67, height=22)
textfield.focus()

# Search icon
Search_icon = PhotoImage(file='img/magnifying_glass.png')
search_button = Button(image=Search_icon, borderwidth=0, cursor='hand2', bg=d_blue, command=get_weather)
search_button.place(x=268, y=65)

# ------ CURRENT WEATHER LABELS (PLACEHOLDERS) -------
# City information label
city_info = Label(text='', font=('Noto Sans', 12), bg=l_blue, fg='white')
city_info.place(x=65, y=97)

# Weather icon label
weather_icon = PhotoImage(file='img/dummy.png')
weather_label = Label(root, image=weather_icon, bg=l_blue)
weather_label.place(x=93, y=130)

# Temperature with ° symbol
temp = Label(text='', font=('Noto Sans', 85, 'bold'), bg=l_blue, fg='white')
temp.place(x=104, y=280, height=111)
temp_symbol = Label(text='', font=('Noto Sans', 20, 'bold'), height=1, bg=l_blue, fg='white')
temp_symbol.place(x=206, y=290, width=15)

condition = Label(text='', font=('Noto Sans', 11), bg=l_blue, fg='white', width=27)
condition.place(x=53, y=390, height=30)

date = Label(text='', font=('Noto Sans', 8), bg=l_blue, fg='white', width=30)
date.place(x=69, y=418, height=15)

# Bottom row
feelslike = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=3)
feelslike.place(x=62, y=487, height=15)

wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
wind.place(x=91, y=487, height=15)

humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=4)
humidity.place(x=152, y=487, height=15)

precipitation = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=4)
precipitation.place(x=197, y=487, height=15)

pressure = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
pressure.place(x=242, y=487, height=15)

root.mainloop()
