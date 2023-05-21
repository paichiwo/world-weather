from datetime import datetime
from tkinter import *
import tkinter as tk
import requests
import calendar
import json
from weather_icons import icons, icons_mini

# Create the window and set the basics
root = Tk()
root.title('World Weather by paichiwo')
root.geometry('350x680+300+200')
root.resizable(False, False)
root.config(bg='black')

# Colors
l_blue = '#1581ef'
d_blue = '#1167f2'


def format_date_long(date):
    """ Format date to weekday, day month_name (Monday, 14 May) """
    date_object = datetime.strptime(date, '%Y-%m-%d')
    week_day = calendar.day_name[date_object.weekday()]
    month = date_object.month
    month_name = calendar.month_name[month]
    return f'{week_day[:3]}, {date_object.day} {month_name}'


def format_date_short(date):
    """ Format date to day month_name (14 May) """
    date_object = datetime.strptime(date, '%Y-%m-%d')
    month = date_object.month
    month_name = calendar.month_name[month]
    return f'{date_object.day} {month_name[:3]}'


def country_code(country_name):
    """ Change full country name to its abbreviation """
    with open('country_code.json') as file:
        json_data = json.load(file)
    for name in json_data:
        if name['Name'] == country_name:
            return name['Code']


def get_weather():
    """ Connect to API, get data and update tkinter labels """
    api_key = 'c5d3e150c44446f3b0c170953232105'
    location = textfield.get()
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=5&aqi=no&alerts=no'
    try:
        data = requests.get(url).json()

        # Info data
        city = data['location']['name']
        country = country_code(data['location']['country'])
        local_time = format_date_long(data['location']['localtime'][:-6])
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
            forecast_date = format_date_short(date_entry['date'])
            forecast_avg_temp = str(int(date_entry['day']['avgtemp_c']))
            forecast_avg_humidity = str(int(date_entry['day']['avghumidity']))
            forecast_max_wind = str(int(date_entry['day']['maxwind_kph']))
            forecast_code = date_entry['day']['condition']['code']

            forecast_data.append([forecast_date,
                                  forecast_avg_temp,
                                  forecast_max_wind,
                                  forecast_avg_humidity,
                                  forecast_code
                                  ])

        # Update current weather labels with data from the API
        city_info.config(text=f'{city}, {country}', fg='white', justify='center', width=22)
        weather_icon.config(file=icons[code])

        if current_is_day == 0:
            weather_icon.config(file=icons[code])
        else:
            weather_icon.config(file=icons[code])  # to update when night icons are made

        temp.config(text=current_temp, justify='center', width=2)

        if len(current_temp) == 1:
            temp_symbol.config(text='°', justify='center')
            temp_symbol.place(x=205, y=290)
        else:
            temp_symbol.config(text='°', justify='center')
            temp_symbol.place(x=238, y=290)

        condition.config(text=current_condition, justify='center')
        date_info.config(text=local_time, justify='center')
        feelslike.config(text=f'{current_feelslike}°', justify='center')
        wind.config(text=f'{current_wind_speed} km/h', justify='center')
        humidity.config(text=f'{current_humidity}%', justify='center')
        precipitation.config(text=f'{current_precipitation} mm', justify='center')
        pressure.config(text=f'{current_pressure} hPa', justify='center')

        # Update forecast weather labels with data from the API
        day_1_date.config(text=forecast_data[0][0], justify='center')
        day_1_temp.config(text=f'{forecast_data[0][1]}°', justify='center')
        day_1_humidity.config(text=f'{forecast_data[0][2]}%', justify='center')
        day_1_wind.config(text=f'{forecast_data[0][3]} km/h', justify='center')
        day_1_icon.config(file=icons_mini[forecast_data[0][4]])

        day_2_date.config(text=forecast_data[1][0], justify='center')
        day_2_temp.config(text=f'{forecast_data[1][1]}°', justify='center')
        day_2_humidity.config(text=f'{forecast_data[1][2]}%', justify='center')
        day_2_wind.config(text=f'{forecast_data[1][3]} km/h', justify='center')
        day_2_icon.config(file=icons_mini[forecast_data[1][4]])

        day_3_date.config(text=forecast_data[2][0], justify='center')
        day_3_temp.config(text=f'{forecast_data[2][1]}°', justify='center')
        day_3_humidity.config(text=f'{forecast_data[2][2]}%', justify='center')
        day_3_wind.config(text=f'{forecast_data[2][3]} km/h', justify='center')
        day_3_icon.config(file=icons_mini[forecast_data[2][4]])

    except KeyError:
        city_info.config(text='Enter correct location', fg='yellow', justify='center', width=22)
    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError) as e:
        city_info.config(text=e, fg='red', justify='center')


# SEARCH BOX
Search_image = PhotoImage(file='img/current_window.png')
search_label = Label(image=Search_image, bg='black')
search_label.place(x=22, y=20)

textfield = tk.Entry(root, justify='center', width=25, font=('Noto Sans', 11, 'bold'), bg=d_blue, border=0, fg='white')
textfield.place(x=60, y=67, height=22)
textfield.focus()
textfield.bind('<Return>', lambda event=None: search_button.invoke())

Search_icon = PhotoImage(file='img/magnifying_glass.png')
search_button = Button(image=Search_icon, activebackground=l_blue, borderwidth=0,
                       cursor='hand2', bg=d_blue, command=get_weather)
search_button.place(x=268, y=65)

# CURRENT WEATHER WINDOW LABELS

# Top row
city_info = Label(text='', font=('Noto Sans', 12), bg=l_blue, fg='white')
city_info.place(x=65, y=97)
weather_icon = PhotoImage(file='img/dummy.png')
weather_label = Label(root, image=weather_icon, bg=l_blue)
weather_label.place(x=95, y=130)
temp = Label(text='', font=('Noto Sans', 85, 'bold'), bg=l_blue, fg='white')
temp.place(x=104, y=280, height=111)
temp_symbol = Label(text='', font=('Noto Sans', 20, 'bold'), height=1, bg=l_blue, fg='white')
temp_symbol.place(x=206, y=290, width=15)
condition = Label(text='', font=('Noto Sans', 11), bg=l_blue, fg='white', width=27)
condition.place(x=53, y=390, height=30)
date_info = Label(text='', font=('Noto Sans', 8), bg=l_blue, fg='white', width=30)
date_info.place(x=69, y=418, height=15)

# Bottom row
feelslike = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=3)
feelslike.place(x=63, y=487, height=15)
wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
wind.place(x=98, y=487, height=15)
humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=4)
humidity.place(x=162, y=487, height=15)
precipitation = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=5)
precipitation.place(x=204, y=487, height=15)
pressure = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
pressure.place(x=250, y=487, height=15)

# FORECAST WINDOW LABELS

day_1_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
day_1_date.place(x=32, y=535, height=20)
day_1_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_1_temp.place(x=37, y=555, height=20)
day_1_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_1_humidity.place(x=37, y=575, height=20)
day_1_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_1_wind.place(x=37, y=595, height=20)
day_1_icon = PhotoImage(file='img/dummy_mini.png')
day_1_icon_label = Label(root, image=day_1_icon, bg='black')
day_1_icon_label.place(x=53, y=618)

day_2_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
day_2_date.place(x=135, y=535, height=20)
day_2_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_2_temp.place(x=140, y=555, height=20)
day_2_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_2_humidity.place(x=140, y=575, height=20)
day_2_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_2_wind.place(x=140, y=595, height=20)
day_2_icon = PhotoImage(file='img/dummy_mini.png')
day_2_icon_label = Label(root, image=day_2_icon, bg='black')
day_2_icon_label.place(x=156, y=618)

day_3_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
day_3_date.place(x=234, y=535, height=20)
day_3_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_3_temp.place(x=239, y=555, height=20)
day_3_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_3_humidity.place(x=239, y=575, height=20)
day_3_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
day_3_wind.place(x=239, y=595, height=20)
day_3_icon = PhotoImage(file='img/dummy_mini.png')
day_3_icon_label = Label(root, image=day_3_icon, bg='black')
day_3_icon_label.place(x=255, y=618)

root.mainloop()
