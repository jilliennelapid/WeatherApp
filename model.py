# The Model can hold raw data, or it will define the essential components of your app.
# Reflects real world things (e.g. For a Task app, Model would define what a task is).

import requests
import json

class Model:
    def __init__(self, api_key):
        self.APIkey = api_key

        self.location = None
        self.entry = None

    # rewrite to check location so error can be produced for incorrect place,
    # remove that check from getWeatherData()
    """
    def checkLocation(self, _location):
        cityName = _location
        url = f'https://api.openweathermap.org/geo/1.0/direct?q={cityName},&limit={3}&appid={self.APIkey}'

        response = requests.get(url)
        data = response.json()

        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f'Invalid Location, please try againHTTP Error: {str(e)}')
    

        country = data[2:3]
        print(country)
        lat = data["lat"]
        lon = data["lon"]

        self.getWeatherData(country, lat, lon)
        
    """

    def getWeatherData(self, _location):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={_location}&appid={self.APIkey}'

        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f'Invalid Location, please try again HTTP Error: {str(e)}')

        data = response.json()

        # print(data)

        return data











