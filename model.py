# The Model can hold raw data, or it will define the essential components of your app.
# Reflects real world things (e.g. For a Task app, Model would define what a task is).

import requests
import pycountry

class Model:
    def __init__(self, api_key):
        self.APIkey = api_key

        self.location = None
        self.entry = None

    def get_country_code(self, _country_name):
        try:
            country = pycountry.countries.lookup(_country_name)
            return getattr(country, 'alpha_2', None)
        except LookupError:
            return None  # Country not found

    def checkLocation(self, _location):
        location_name, country_name = _location.split(', ')
        print(country_name)
        country_alpha2 = self.get_country_code(country_name)

        url = f'https://api.openweathermap.org/geo/1.0/direct?q={location_name},&limit={5}&appid={self.APIkey}'

        response = requests.get(url)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f'Invalid Location, please try again HTTP Error: {str(e)}')
        else:
            data = response.json()

        lat = lon = 0
        print(data)
        print(country_alpha2)

        # Verifying the correct Country/State that the city belongs to.
        # Then getting the Latitude and Longitude for that city
        for location in data:
            state = location.get('state')  # Use .get() to avoid KeyError
            country = location.get('country')  # Use .get() for country too

            if state == country_name or country == country_alpha2:
                lat = location.get('lat', 0)  # Default to 0 if 'lat' doesn't exist
                lon = location.get('lon', 0)  # Default to 0 if 'lon' doesn't exist
                break

        return lat, lon

    def getWeatherData(self, _lat, _lon):
        # units =
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={_lat}&lon={_lon}&appid={self.APIkey}&units=imperial'

        response = requests.get(url)
        data = response.json()

        print(data)

        return data











