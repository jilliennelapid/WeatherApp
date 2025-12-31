# The Controller acts as a liaison between the Model and the View,
# receiving user input and deciding what to do with it.
from view import MainView, StatsView

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.main_view = None
        self.stats_view = None

    # Connecting the Frame objects to allow updates
    def set_frames(self, view):
        self.main_view = view.frames[MainView]
        self.stats_view = view.frames[StatsView]

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