# The Controller acts as a liaison between the Model and the View,
# receiving user input and deciding what to do with it.

# Will call functions from model and view using the objects passed
# into the constructor. try/except blocks?

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load(self, location):
        self.model.location = location
        self.model.callLocation(location)

        self.model.getWeatherData()




