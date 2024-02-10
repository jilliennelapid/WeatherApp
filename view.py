# The View defines the code for the display or features that the
# user interacts with.
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from datetime import datetime

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

        self.save_button = ctk.CTkButton(self, corner_radius=10, text='Search', command=self.search_button_clicked)
        self.save_button.grid(row=0, column=2, padx=10)

        self.status_label = ttk.Label(self, text='', foreground='yellow')
        self.status_label.grid(row=1, column=1, sticky=tk.W)

        self.weather_label = ttk.Label(self, text='')
        self.weather_label.grid(row=2, column=1, sticky=tk.W)

        self.temperature_label = ttk.Label(self, text='')
        self.temperature_label.grid(row=3, column=1, sticky=tk.W)

        self.temp_min_label = ttk.Label(self, text='')
        self.temp_min_label.grid(row=3, column=2, sticky=tk.W)

        self.temp_max_label = ttk.Label(self, text='')
        self.temp_max_label.grid(row=4, column=1, sticky=tk.W)

        self.rain_label = ttk.Label(self, text='')
        self.rain_label.grid(row=4, column=2, sticky=tk.W)

        self.wind_speed_label = ttk.Label(self, text='')
        self.wind_speed_label.grid(row=5, column=1, sticky=tk.W)

        self.humidity_label= ttk.Label(self, text='')
        self.humidity_label.grid(row=5, column=2, sticky=tk.W)

        self.sunrise_label = ttk.Label(self, text='')
        self.sunrise_label.grid(row=6, column=1, sticky=tk.W)

        self.sunset_label = ttk.Label(self, text='')
        self.sunset_label.grid(row=6, column=2, sticky=tk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def search_button_clicked(self):
        if self.controller:
            self.controller.load(self.location.get())

    def show_message(self, message):
        self.status_label['text'] = message
        self.status_label['foreground'] = 'yellow'
        self.status_label.after(5000, self.hide_message)

        """
        # reset the form
        self.email_entry['foreground'] = 'black'
        self.email_var.set('')
        """

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.status_label['text'] = ''

    def set_weather(self, data):
        weather = data['weather'][0]['description']
        self.weather_label['text'] = weather

    def set_temperature(self, data):
        temperature = int(data['main']['temp'])
        self.temperature_label['text'] = temperature

    def set_temp_min(self, data):
        temp_min = int(data['main']['temp_min'])
        self.temp_min_label['text'] = temp_min

    def set_temp_max(self, data):
        temp_max = int(data['main']['temp_max'])
        self.temp_max_label['text'] = temp_max

    def set_rain(self, data):
        try:
            rain = data['rain']['1h']
        except KeyError:
            rain = "N/A"

        self.rain_label['text'] = rain

    def set_windSpeed(self, data):
        wind_speed = data['wind']['speed']
        self.wind_speed_label['text'] = wind_speed

    def set_humidity(self, data):
        humidity = data['main']['humidity']
        self.humidity_label['text'] = humidity

    def set_sunrise(self, data):
        sunrise = data['sys']['sunrise']

        convertedTime = datetime.fromtimestamp(sunrise)

        self.sunrise_label['text'] = convertedTime

    def set_sunset(self, data):
        sunset = data['sys']['sunset']

        convertedTime = datetime.fromtimestamp(sunset)

        self.sunset_label['text'] = convertedTime

    # def set_lastUpdate_time(self):
