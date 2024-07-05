# WeatherApp
WeatherApp is a Python program able to display weather data for a desired city/town in a certain country.

The program makes use of `tkinter` and `customtkinter` to build the GUI, [OpenWeather](https://openweathermap.org) API for the weather data, and model-view-controller for the code organization.

___

## Running the Program
Python 3.12 was used for building this program.

An API Key from OpenWeather must be used for the acquisition of weather data. OpenWeather has tiered plans for use of their API depending on how many calls you make per minute and per month. Testing of this program has made use of their [Free](https://openweathermap.org/price#weather) plan which provides 60 calls per minute and 1,000,000 calls per month. It provides the basics such as [Current Weather](https://openweathermap.org/current) and [3-hour step Forecast, over 5 days](https://openweathermap.org/forecast5).

### Setting up an OpenWeather API Key
1) Create an account on [OpenWeather](https://openweathermap.org) for free.
2) Direct yourself to their [`Pricing`](https://openweathermap.org/price) page. Select your appropriate plan.
3) Copy the API Key. This key will also be visible by clicking on your username and selecting 'My API Keys' .
   > (Tip: DO NOT share this key or any similar API Keys with others, such as by uploading your key to online repositories).
5) Add the API Key to a `.env` file. Make the first line in the file `APIkey=#####` with the hashes representing your key.

### Setting up the Files
1) Fork and clone the repository. You may also directly download the files in this repository.
2) Ensure that your `.env` file is set up in the same file location as `main.py`, `model.py`, `view.py`, and `controller.py`.
3) Run `main.py` in your IDE of choice OR open your command line (or equivalent), navigate to the directory, and run
   
   `python3.12 main.py`.

