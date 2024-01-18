# The Model can hold raw data, or it will define the essential components of your app.
# Reflects real world things (e.g. For a Task app, Model would define what a task is).
class Model():
    def __init__(self):
        self.location = None

        self.entry = None


    def getData(self):
        # make api call here