## **Weather App with PySimpleGUI**

This is a simple Python app that displays the current weather information for a given location, using the [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) library for the GUI and the [Weatherstack](https://weatherstack.com/) API for the weather data.

The app displays a window with three columns: an image column with an icon representing the current weather condition, and two info columns with details about the temperature, wind, humidity, etc. The user can input a location in a text field, and click a button to update the weather information.

## **Prerequisites**

To run this app, you need to have Python 3.x and PySimpleGUI installed. You also need to sign up for a free API key from [Weatherstack](https://weatherstack.com/) and paste it in the **api\_key** variable in the code.

You can install PySimpleGUI via pip:

bashCopy code

`pip install pysimplegui`

## **How to Run**

To run the app, open a terminal in the folder containing the code file, and type:

bashCopy code

`python weather_app.py`

This should open the app window. You can enter a location (e.g., "London, UK") in the input field, and click the "Search" button to update the weather information.

## **How to Customize**

You can customize the app by changing the images in the **weather\_icons** dictionary to match your own icons, or by modifying the GUI layout in the **create\_window** function. You can also change the theme of the app by passing a different theme name to the **sg.theme** function in the **create\_window** function. The available theme names are listed in the [PySimpleGUI documentation](https://pysimplegui.readthedocs.io/en/latest/#themes).

## **License**

This app is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute it as you like.

## **Example Output**

![](https://33333.cdn.cke-cs.com/kSW7V9NHUXugvhoQeFaf/images/3a0f3730416b8a0155368619938f09f0c6ad393af571ce6e.png)