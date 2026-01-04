# The View defines the code for the display or features that the
# user interacts with.
import customtkinter as ctk
from datetime import datetime
from PIL import Image
import json

class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        #ctk.CTk.__init__(self, *args, **kwargs)

        self.window = ctk.CTkFrame(self)
        self.window.pack(side="top", fill="both", expand=True)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Initializing frames to an empty array
        self.frames = {}

        # Iterating through a tuple consisting of
        # the different page layouts
        for F in (MainView, StatsView, SettingsView, SavedView):
            frame = F(self.window, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainView)
        self.controller = None

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_controller(self, controller):
        self.controller = controller

class MainView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent")

        # Main Menu Options Frame
        self.main_menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_menu_frame.grid(row=0, column=0, sticky='nsew', padx=30, pady=10)
        self.main_menu_frame.grid_columnconfigure(0, weight=1)

        self.main_icon_img = ctk.CTkImage(light_image=Image.open("images/main-app-icon.png"), size=(265, 130))
        self.main_icon = ctk.CTkLabel(self.main_menu_frame, image=self.main_icon_img, text="")
        self.main_icon.grid(row=0, column=0, rowspan=2, padx=30, pady=10, sticky="nsew")

        self.saved_locations_button_img = ctk.CTkImage(light_image=Image.open("images/saved-locations-icon-light.png"),
                                                       dark_image=Image.open("images/saved-locations-icon-dark.png"),
                                                       size=(195, 42))
        self.saved_locations_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.saved_locations_button_img,
                                                    text="", command=lambda:view_control.show_frame(SavedView),
                                                    fg_color="transparent", hover=False)
        self.saved_locations_button.grid(row=0, column=1, padx=30, pady=10)

        self.settings_button_img = ctk.CTkImage(light_image=Image.open("images/settings-icon-light.png"),
                                                dark_image=Image.open("images/settings-icon-dark.png"),
                                                size=(195, 42))
        self.settings_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.settings_button_img,
                                             text="", command=lambda:view_control.show_frame(SettingsView),
                                             fg_color="transparent", hover=False)
        self.settings_button.grid(row=1, column=1, padx=30, pady=10)

        # Search Bar Frame
        self.search_bar_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.search_bar_frame.grid(row=3, column=0, padx=30, pady=(0, 30))

        self.label = ctk.CTkLabel(self.search_bar_frame, text='Enter a Location:')
        self.label.grid(row=1, column=0)

        self.location = ctk.StringVar()
        self.location_search = ctk.CTkEntry(self.search_bar_frame, textvariable=self.location, width=200)
        self.location_search.grid(row=1, column=1, sticky='nsew', padx=10)

        self.location_search.insert(0, 'City Name, State/Country')
        self.location_search.bind('<FocusIn>', self.on_entry_click)
        self.location_search.bind('<Return>', self.search_button_clicked)

        self.search_button = ctk.CTkButton(self.search_bar_frame, corner_radius=10, text='Search',
                                           command=self.search_button_clicked, fg_color="#5989d7",
                                           hover_color="#496fae")
        self.search_button.grid(row=1, column=3, padx=40)

        self.status_label = ctk.CTkLabel(self.search_bar_frame, text='')
        self.status_label.grid(row=1, column=1, sticky=ctk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def on_entry_click(self, event):
        self.location_search.delete(0, "end")  # delete all the text in the entry
        self.location_search['foreground'] = 'black'

    # Begins the Search Logic upon clicking 'Search' or pressing enter
    def search_button_clicked(self):
        if self.controller:
            self.controller.load(self.location.get())

    def show_message(self, message):
        self.status_label['text'] = message
        self.status_label['foreground'] = 'yellow'
        self.status_label.after(5000, self.hide_message)

    def hide_message(self):
        self.status_label['text'] = ''


# Displays the Weather Stats after user looks up a location
class StatsView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        # Weather Data Frame
        self.info_widgets_frame = ctk.CTkFrame(self)
        self.info_widgets_frame.grid(row=0, column=0, stick='nsew')

        # Location Name
        self.location_label = ctk.CTkLabel(self.info_widgets_frame, text="")
        self.location_label.grid(row=0, column=1, sticky=ctk.W)

        # Temperature (in degrees)
        self.temperature_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temperature_label.grid(row=1, column=1, sticky=ctk.W)

        # Label of Weather Type
        self.weather_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.weather_label.grid(row=2, column=1, sticky=ctk.W)

        # Lowest Temperature for the Day
        self.temp_min_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_min_label.grid(row=1, column=2, sticky=ctk.W)

        self.temp_min_value = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_min_value.grid(row=4, column=0, sticky=ctk.W)
        self.temp_max_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_max_label.grid(row=4, column=1, sticky=ctk.W)

        self.rain_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.rain_label.grid(row=4, column=2, sticky=ctk.W)

        self.wind_speed_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.wind_speed_label.grid(row=5, column=1, sticky=ctk.W)

        self.humidity_label= ctk.CTkLabel(self.info_widgets_frame, text='')
        self.humidity_label.grid(row=5, column=2, sticky=ctk.W)

        self.sunrise_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.sunrise_label.grid(row=6, column=1, sticky=ctk.W)

        self.sunset_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.sunset_label.grid(row=6, column=2, sticky=ctk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def set_location_name(self, data):
        location = data['name']
        self.location_label['text'] = location

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

class SavedView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        self.label = ctk.CTkLabel(self, text="Saved View", font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=1, column=0, padx=40)

        #ctk.set_appearance_mode("Dark")
        #self.saved_menu = ctk.CTkFrame(parent)

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)
        self.use_sys_mode = ctk.IntVar()
        self.night_mode = ctk.IntVar()

        self.pull_setting_pref()

        # Label of the Frame
        self.frame_label = ctk.CTkLabel(self, text="Settings View", font=("Arial", 16, "bold"))
        self.frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 1) System/Manual Mode Toggle - Label
        self.mode_label = ctk.CTkLabel(self, text="Use System Default Mode", font=("Arial", 14))
        self.mode_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # 1) System/Manual Mode Toggle - Check Box
        self.mode_toggle = ctk.CTkCheckBox(self, text="", command=self.set_sys_mode, variable=self.use_sys_mode,
                                           onvalue=1, offvalue=0)
        self.mode_toggle.grid(row=1, column=2, padx=40, pady=20, sticky="w")

        # 2) Light/Dark Mode Toggle - Label
        self.toggle_label = ctk.CTkLabel(self, text="Theme Toggle", font=("Arial", 14))
        self.toggle_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # 2) Light/Dark Mode Toggle - Switch
        self.mode_switch = ctk.CTkSwitch(self, width=10, height=10, text="", command=self.set_dark_mode,
                                         variable=self.night_mode, onvalue=1, offvalue=0)
        self.mode_switch.grid(row=2, column=2, padx=40, pady=20, sticky="w")

        self.grid_columnconfigure(2, weight=1)

        # Return to Home Button
        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home',
                                           command=lambda:view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=5, column=2, columnspan=2, padx=40, pady=20, sticky="e")


        self.set_widget_state()
        #self.settings_menu = ctk.CTkFrame(parent)


    def pull_setting_pref(self):
        file_path = "data/settings.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            self.use_sys_mode.set(int(data['system_mode']['in_use']))
            self.night_mode.set(int(data['night_mode']['in_use']))

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file {file_path}: {e}.")

    def set_widget_state(self):
        if self.use_sys_mode.get() == 1:
            ctk.set_appearance_mode("System")
            self.mode_switch.configure(state="disabled")

        elif self.use_sys_mode.get() == 0:
            if self.night_mode.get() == 0:
                ctk.set_appearance_mode("Light")

            elif self.night_mode.get() == 1:
                ctk.set_appearance_mode("Dark")

            self.mode_switch.configure(state="normal")

    def set_sys_mode(self):
        if self.use_sys_mode.get() == 1:
            ctk.set_appearance_mode("System")
            self.update_json("system_mode", 1)
            self.mode_switch.configure(state="disabled")

        elif self.use_sys_mode.get() == 0:
            self.mode_switch.configure(state="normal")
            self.update_json("system_mode", 0)
            self.set_dark_mode()

    def set_dark_mode(self):
        if self.night_mode.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.update_json("night_mode", self.night_mode.get())

        elif self.night_mode.get() == 0:
            ctk.set_appearance_mode("Light")
            self.update_json("night_mode", self.night_mode.get())

    def update_json(self, field, new_value):
        file_path = "data/settings.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file {file_path}: {e}.")

        data[field]['in_use'] = new_value

        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

        except IOError as e:
            print(f"Error writing to {file_path}: {e}")
