#!/usr/bin/env python3

# World Weather GUI

import PySimpleGUI as sg
import requests

# icon collection:
weather_icons = {
    0: "images/Cloudy.png",
    1: "images/Rain.png",
    2: "images/Haze.png",
    3: "images/Part_cloud.png",
    4: "images/Drizzle.png",
    5: "images/Snow.png",
    6: "images/Sunny.png",
    7: "images/Thunder.png",
    8: "images/splash.png"
}


def convert_12_to_24(twelve):
    # Convert 12-hour format "05:34 PM' to 24-hour format "17:34"

    if twelve[-2:] == "AM" and twelve[:2] == "12":
        return "00" + twelve[2:-3]

    elif twelve[-2:] == "PM" and twelve[:2] == "12":
        return twelve[:-3]

    elif twelve[-2:] == "AM":
        return twelve[:-3]

    else:
        return str(int(twelve[:2]) + 12) + twelve[2:-3]


def get_weather_data(location):

    api_key = ""  # Your API key goes here
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location.replace(' ', '')}, language=PL"
    response = requests.get(url)
    json_dict = response.json()
    # GET DATA FOR:

    weather_desc = json_dict["current"]["weather_descriptions"][0]

    cty = json_dict["location"]["name"]
    cntr = json_dict["location"]["country"]
    dn = json_dict["current"]["is_day"]
    lt = json_dict["location"]["localtime"]
    temp = json_dict["current"]["temperature"]
    fl = json_dict["current"]["feelslike"]
    hu = json_dict["current"]["humidity"]
    ot = json_dict["current"]["observation_time"]
    ws = json_dict["current"]["wind_speed"]
    wd = json_dict["current"]["wind_dir"]
    pr = json_dict["current"]["pressure"]
    cc = json_dict["current"]["cloudcover"]
    pre = json_dict["current"]["precip"]
    vis = json_dict["current"]["visibility"]

    return weather_desc, cty, cntr, dn, lt, temp, fl, hu, ot, ws, wd, pr, cc, pre, vis


def create_window(theme):

    sg.theme(theme)
    font_1 = "Calibri"
    image_column = sg.Column([
        [sg.Push(), sg.Text("", key="-DESCRIPTION-", font="Calibri 10"), sg.Push()],
        [sg.Image(weather_icons[8], key="-IMAGE-")]

    ])

    info_column_1 = sg.Column([
        [sg.Push(), sg.Text("", key="-CITY-", font="Calibri 18", text_color="yellow"), sg.Push()],
        [sg.Text("Local time:"), sg.Push(), sg.Text("", key="-LOCALTIME-")],
        [sg.Text("Temperature:"), sg.Push(), sg.Text("", key="-TEMPERATURE-")],
        [sg.Text("Real feel:"), sg.Push(), sg.Text("", key="-FEELS-LIKE-")],
        [sg.Text("Pressure:"), sg.Push(), sg.Text("", key="-PRESSURE-")],
        [sg.Text("Humidity:"), sg.Push(), sg.Text("", key="-HUMIDITY-")],
        [sg.VPush()]
    ])
    info_column_2 = sg.Column([
        [sg.Push(), sg.Text("", key="-COUNTRY-", font="Calibri 18", text_color="yellow"), sg.Push()],
        [sg.Text("Wind/Direction:"), sg.Push(), sg.Text("", key="-WIND-SPEED-"), sg.Text("", key="-WIND-DIRECTION-")],
        [sg.Text("Cloud cover:"), sg.Push(), sg.Text("", key="-CLOUD-COVER-")],
        [sg.Text("Visibility:"), sg.Push(), sg.Text("", key="-VISIBILITY-")],
        [sg.Text("Precipitation:"), sg.Push(), sg.Text("", key="-PRECIP-")],
        [sg.Text("Observation:"), sg.Push(), sg.Text("", key="-OBSERVATION-TIME-")],
        [sg.VPush()]
    ])
    layout = [
        [sg.Input("", key="-INPUT-"), sg.Button("Search", key="-CLICK-", border_width=0)],
        [sg.Text("Example - London, UK", font="Calibri 10", text_color="grey")],
        [image_column, info_column_1, info_column_2]
    ]

    return sg.Window("World Weather", layout, size=(700, 300),
                     element_justification="center", font=font_1,
                     finalize=True)


window = create_window("DarkBlue12")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-CLICK-":
        (weather_description, city, country, day_night, local_time,
         temperature, feels_like, humidity, observation_time, wind_speed,
         wind_direction, pressure, cloud_cover, precip, visibility) = get_weather_data(values['-INPUT-'])

        window["-CITY-"].update(city.upper())
        window["-COUNTRY-"].update(country.upper())
        window["-LOCALTIME-"].update(local_time[11:])
        window["-TEMPERATURE-"].update(f"{temperature} °C")
        window["-FEELS-LIKE-"].update(f"{feels_like} °C")
        window["-HUMIDITY-"].update(f"{humidity} %")
        window["-WIND-SPEED-"].update(f"{wind_speed} km/h")
        window["-WIND-DIRECTION-"].update(wind_direction)
        window["-PRESSURE-"].update(f"{pressure} hPa")
        window["-CLOUD-COVER-"].update(f"{cloud_cover} %")
        window["-VISIBILITY-"].update(f"{visibility} %")
        window["-PRECIP-"].update(f"{precip} %")
        window["-OBSERVATION-TIME-"].update(convert_12_to_24(observation_time))
        window["-DESCRIPTION-"].update(weather_description)

        # weather image update conditions
        # sun
        if weather_description in ('Sun', 'Sunny', 'Clear', 'Clear with periodic clouds', 'Mostly sunny'):
            window['-IMAGE-'].update(weather_icons[6])

        # cloud
        if weather_description in ('Mostly cloudy', 'Cloudy', 'Overcast'):
            window['-IMAGE-'].update(weather_icons[0])
        # part sun
        if weather_description in ('Partly Sunny', 'Mostly Sunny', 'Partly cloudy'):
            window['-IMAGE-'].update(weather_icons[3])

        # rain
        if weather_description in ('Rain', 'Showers', 'Scattered Showers', 'Rain and Snow', 'Hail'):
            window['-IMAGE-'].update(weather_icons[1])

        # light rain
        if weather_description in ('Light Rain', 'Chance of Rain', 'Light rain shower'):
            window['-IMAGE-'].update(weather_icons[4])

        # thunder
        if weather_description in ('Scattered Thunderstorms', 'Chance of Storm',
                                   'Storm', 'Thunderstorm', 'Chance of TStorm'):
            window['-IMAGE-'].update(weather_icons[7])

        # foggy
        if weather_description in ('Mist', 'Dust', 'Fog', 'Smoke', 'Haze', 'Flurries'):
            window['-IMAGE-'].update(weather_icons[2])

        # snow
        if weather_description in ('Freezing Drizzle', 'Light snow', 'Chance of Snow',
                                   'Sleet', 'Snow', 'Icy', 'Snow Showers', 'Moderate snow'):
            window['-IMAGE-'].update(weather_icons[5])

window.close()
