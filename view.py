# The View defines the code for the display or features that the
# user interacts with.
import tkinter as tk
from tkinter import ttk

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text='Enter a Location:')
        self.label.grid(row=0, column=0)

        # Initializes the variable locations as a tkinter string variable
        self.location = tk.StringVar()
        # (frame, variable entry is saved to, size)
        self.location_search = ttk.Entry(self, textvariable=self.location, width=30)
        self.location_search.grid(row=0, column=1, sticky=tk.NSEW)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def load_button_clicked(self):
        if self.controller:
            self.controller.load(self.location.get())

    def set_weather(self):

    def set_temperature(self):

    def set_rain(self):

    def set_windSpeed(self):

    def set_humidity(self):

    def set_sunrise(self):

    def set_sunset(self):

    def set_lastUpdate_time(self):
