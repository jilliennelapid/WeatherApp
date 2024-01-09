# The Controller acts as a liaison between the Model and the View,
# receiving user input and deciding what to do with it.

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view