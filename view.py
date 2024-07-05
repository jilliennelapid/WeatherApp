# The View defines the code for the display or features that the
# user interacts with.
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Search Bar Frame
        self.search_bar_frame = ttk.Frame(parent, width=500, height=100)
        self.search_bar_frame.grid(row=0, column=0, padx=30, pady=10)

        self.label = ttk.Label(self.search_bar_frame, text='Enter a Location:')
        self.label.grid(row=0, column=0)

        self.location = tk.StringVar()
        self.location_search = ttk.Entry(self.search_bar_frame, textvariable=self.location, width=35, foreground='gray')
        self.location_search.grid(row=0, column=1, sticky=tk.NSEW)

        self.location_search.insert(0, 'Enter a location as: "Location, Country/State"')
        self.location_search.bind('<FocusIn>', self.on_entry_click)
        self.location_search.bind('<Return>', self.on_enter_pressed)

        self.search_button = ctk.CTkButton(self.search_bar_frame, corner_radius=10, text='Search',
                                           command=self.search_button_clicked, fg_color="#5989d7",
                                           hover_color="#496fae")
        self.search_button.grid(row=0, column=2, padx=30)

        self.status_label = ttk.Label(self.search_bar_frame, text='', foreground='yellow')
        self.status_label.grid(row=1, column=1, sticky=tk.W)

        # Weather Data Frame
        self.info_widgets_frame = ttk.Frame(parent, width=500, height=200)
        self.info_widgets_frame.grid(row=2, column=0, padx=30, pady=30)

        self.weather_label = ttk.Label(self.info_widgets_frame, text='')
        self.weather_label.grid(row=2, column=1, sticky=tk.W)

        self.temperature_label = ttk.Label(self.info_widgets_frame, text='')
        self.temperature_label.grid(row=3, column=1, sticky=tk.W)

        self.temp_min_label = ttk.Label(self.info_widgets_frame, text='')
        self.temp_min_label.grid(row=3, column=2, sticky=tk.W)

        self.temp_max_label = ttk.Label(self.info_widgets_frame, text='')
        self.temp_max_label.grid(row=4, column=1, sticky=tk.W)

        self.rain_label = ttk.Label(self.info_widgets_frame, text='')
        self.rain_label.grid(row=4, column=2, sticky=tk.W)

        self.wind_speed_label = ttk.Label(self.info_widgets_frame, text='')
        self.wind_speed_label.grid(row=5, column=1, sticky=tk.W)

        self.humidity_label= ttk.Label(self.info_widgets_frame, text='')
        self.humidity_label.grid(row=5, column=2, sticky=tk.W)

        self.sunrise_label = ttk.Label(self.info_widgets_frame, text='')
        self.sunrise_label.grid(row=6, column=1, sticky=tk.W)

        self.sunset_label = ttk.Label(self.info_widgets_frame, text='')
        self.sunset_label.grid(row=6, column=2, sticky=tk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def on_entry_click(self, event):
        self.location_search.delete(0, "end")  # delete all the text in the entry
        self.location_search['foreground'] = 'white'

    def on_enter_pressed(self, event):
        if self.controller:
            self.controller.load(self.location.get())

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
