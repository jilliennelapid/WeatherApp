# WeatherApp
WeatherApp is a Python program in development meant to display weather data for a desired city/town in a certain country.

The program makes use of `customtkinter` to build the GUI, [OpenWeather](https://openweathermap.org) API for the weather data, and model-view-controller for the code organization.
This project also provided me with basic experience working with Adobe Illustrator to make the icons and buttons in the app.

___

## Running the Program
Python 3.12 was used for building this program, with development being done in JetBrain's Python IDE, [PyCharm](https://www.jetbrains.com/pycharm/), which is free to use.

An API Key from OpenWeather must be used for the acquisition of weather data. OpenWeather has tiered plans for use of their API depending on how many calls you make per minute and per month. 

This program implements their [Free Plan](https://openweathermap.org/price#weather) which provides 60 calls per minute and 1,000,000 calls per month. It provides the basics such as [Current Weather](https://openweathermap.org/current) and [3-hour step Forecast, over 5 days](https://openweathermap.org/forecast5).

### 1) Setting up an OpenWeather API Key
1) Create an account on [OpenWeather](https://openweathermap.org) for free.
2) Direct yourself to their [`Pricing`](https://openweathermap.org/price) page. Select your appropriate plan.
3) Copy the API Key for Step 2). This key will also be visible by clicking on your username and selecting 'My API Keys' .
   > (Tip: DO NOT share this key or any similar API Keys with others, such as by uploading your key to online repositories).

### 2) Setting up the Files
1) Fork and clone the repository. You may also directly download the files in this repository.
2) Open or enter into the repository on your local computer.
3) Create a `.env` file in the repository. Make the first line in the file `APIkey=#####` where the hashes (`#####`) represent your copied OpenWeather API key.
   > Ensure that your `.env` file is set up in the same file location as the python files `main.py`, `model.py`, `view.py`, and `controller.py`, as well as the folders `/data` and `/images`.
4) Start WeatherApp by running `main.py` in your IDE of choice OR open your command line (or equivalent application), navigate to the directory, and run

   `python3.12 main.py`.

