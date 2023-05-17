from datetime import datetime
from tkinter import *
import tkinter as tk
import requests
import calendar
import json
from weather_icons import icons

# root window
root = Tk()
root.title("Title")
root.geometry("350x680+300+200")
root.resizable(False, False)
root.config(bg="black")

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


def country_code(country_name):
    """ Change full country name to its abbreviation """
    with open("country_code.json") as file:
        json_data = json.load(file)

    for name in json_data:
        if name["Name"] == country_name:
            return name["Code"]


def get_weather():
    api_key = "58426b1c8989446e9b7142031230103"
    location = textfield.get()
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&aqi=no&alerts=no"
    response = requests.get(url)
    data = response.json()

    # Info data
    city = data['location']['name']
    country = country_code(data['location']['country'])
    local_time = format_date(data['location']['localtime'][:-6])

    # Current data
    code = data['current']['condition']['code']
    current_temp = str(int(data['current']['temp_c']))
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

    city_info.config(text=f"{city}, {country}", justify="center", width=22)
    weather_icon.config(file=icons[code])
    temp.config(text=current_temp+"°", justify='center', bg=l_blue, fg='white', width=2)


# colors
l_blue = "#1581ef"
d_blue = "#1167f2"

# search box
Search_image = PhotoImage(file="img/current_window.png")
search_label = Label(image=Search_image, bg="black")
search_label.place(x=22, y=20)
# input field
textfield = tk.Entry(root, justify="center",width=25,font=("Noto Sans", 11, "bold"),bg=d_blue, border=0, fg="white")
textfield.place(x=60, y=67, height=22)
textfield.focus()
# search icon
Search_icon = PhotoImage(file="img/magnifying_glass.png")
search_button = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg=d_blue, command=get_weather)
search_button.place(x=268, y=65)

# Labels
# label1 = Label(root, text="WIND", font=("Noto Sans", 12), fg="#FFFFFF", bg="#1AB5EF")
# label1.place(x=120, y=400)

# my data
city_info = Label(text="", font=("Noto Sans", 12), bg=l_blue, fg="white")
city_info.place(x=65, y=97)

weather_icon = PhotoImage(file='img/dummy.png')
weather_label = Label(root, image=weather_icon, bg=l_blue)
weather_label.place(x=95, y=130)

temp = Label(text="", font=("Noto Sans", 85, "bold"), bg=l_blue, fg="white")
temp.place(x=120, y=280, height=111)


condition = Label(font=("Noto Sans", 12, "bold"))
condition.place(x=400, y=250)


root.mainloop()
