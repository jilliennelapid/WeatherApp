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
    def checkLocation(self, _location):
        location_name, country_name = _location.split(', ')
        print(location_name + "\n" + country_name)

        url = f'https://api.openweathermap.org/geo/1.0/direct?q={location_name},&limit={5}&appid={self.APIkey}'

        response = requests.get(url)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f'Invalid Location, please try again HTTP Error: {str(e)}')
        else:
            data = response.json()

        lat = lon = 0

        for location in data:
            if location['state'] == country_name:
                lat = location["lat"]
                lon = location["lon"]
                break

        return lat, lon

    def getWeatherData(self, _lat, _lon):
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={_lat}&lon={_lon}&appid={self.APIkey}&units=imperial'

        response = requests.get(url)

        data = response.json()

        print(data)

        return data











