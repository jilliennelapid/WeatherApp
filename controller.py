# The Controller acts as a liaison between the Model and the View,
# receiving user input and deciding what to do with it.

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load(self, location):
        try:
            self.model.location = location
            lat, lon = self.model.checkLocation(location)
        except ValueError as error:
            self.view.show_message(error)
        else:
            results = self.model.getWeatherData(lat, lon)

            self.view.set_weather(results)
            self.view.set_temperature(results)
            self.view.set_temp_min(results)
            self.view.set_temp_max(results)
            self.view.set_rain(results)
            self.view.set_windSpeed(results)
            self.view.set_humidity(results)
            self.view.set_sunrise(results)
            self.view.set_sunset(results)