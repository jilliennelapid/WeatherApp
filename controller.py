# The Controller acts as a liaison between the Model and the View,
# receiving user input and deciding what to do with it.
from view import MainView, StatsView, SavedView, LoadView

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.main_view = None
        self.stats_view = None
        self.saved_view = None

        self.set_frames(self.view)

    # Connecting the Frame objects to allow updates
    def set_frames(self, view):
        self.main_view = view.frames[MainView]
        self.stats_view = view.frames[StatsView]
        self.saved_view = view.frames[SavedView]

    def load(self, location, origin):
        try:
            self.model.location = location
            lat, lon = self.model.checkLocation(location)
        except ValueError as error:
            self.main_view.show_message(error)
        else:
            results = self.model.getWeatherData(lat, lon)

            #print(results)
            self.view.show_frame(LoadView)

            self.stats_view.set_location_name(location)
            self.stats_view.set_weather(results)
            self.stats_view.set_temperature(results)
            self.stats_view.set_temp_min(results)
            self.stats_view.set_temp_max(results)
            self.stats_view.set_rain(results)
            self.stats_view.set_windSpeed(results)
            self.stats_view.set_humidity(results)
            self.stats_view.set_sunrise(results)
            self.stats_view.set_sunset(results)

            self.stats_view.set_return_button(self.view, origin)

            # Look for if a location is already saved here
            self.view.show_frame(StatsView)