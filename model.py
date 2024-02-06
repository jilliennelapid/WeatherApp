# The Model can hold raw data, or it will define the essential components of your app.
# Reflects real world things (e.g. For a Task app, Model would define what a task is).

import requests

class Model:
    def __init__(self, api_key):
        self.APIkey = api_key

        self.location = None
        self.entry = None



    def callLocation(self, _location):
        cityName = _location
        url = f'https://api.openweathermap.org/geo/1.0/direct?q={cityName},&limit={3}&appid={self.APIkey}'

        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e) + "\nEnter a new location."        # Might need to rewrite to display in GUI
        else:
            data = response.json()

        country = data['state']
        lat = data['lat']
        lon = data['lon']

        self.getWeatherData(country, lat, lon)

    def getWeatherData(self, _country, _lat, _lon):
        country = _country
        lat = _lat
        lon = _lon


        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.APIkey}'

        res = requests.get(url)
        data = res.json()

        weather = data['weather']['description']
        temperature = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_min = data['main']['temp_max']
        rain = data['rain']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        sunrise = data['sys']['sunrise']
        sunset = data['sunset']











