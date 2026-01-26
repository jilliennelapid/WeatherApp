# The View defines the code for the display or features that the
# user interacts with.
import customtkinter as ctk
from datetime import datetime
from PIL import Image
import json

globalFont = "Helvetica"

class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.window = ctk.CTkFrame(self, fg_color="transparent")
        self.window.pack(side="top", fill="both", expand=True)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=0)

        # Initializing frames to an empty array
        self.frames = {}

        # Iterating through a tuple consisting of
        # the different page layouts
        for F in (LoadView, MainView, StatsView, SettingsView, SavedView):
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
        self.frames[MainView].set_controller(self.controller)
        self.frames[StatsView].set_controller(self.controller)
        self.frames[SavedView].set_controller(self.controller)

# Buffer Frame while elements are loading on another frame
class LoadView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent")

class MainView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent")

        # Main Menu Options Frame
        self.main_menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_menu_frame.grid(row=0, column=0, sticky='nsew', padx=30, pady=(20,10))
        self.main_menu_frame.grid_columnconfigure(0, weight=1)
        self.main_menu_frame.bind("<Button-1>", lambda y, w=self.main_menu_frame: self.leave_entry(w))

        self.main_icon_img = ctk.CTkImage(light_image=Image.open("images/main-app-icon.png"), size=(265, 130))
        self.main_icon = ctk.CTkLabel(self.main_menu_frame, image=self.main_icon_img, text="")
        self.main_icon.grid(row=0, column=0, rowspan=2, padx=30, pady=10, sticky="nsew")

        self.saved_locations_button_img = ctk.CTkImage(dark_image=Image.open("images/saved-locations-icon-light.png"),
                                                       light_image=Image.open("images/saved-locations-icon-dark.png"),
                                                       size=(195, 42))
        self.saved_locations_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.saved_locations_button_img,
                                                    text="", command=lambda:view_control.show_frame(SavedView),
                                                    fg_color="transparent", hover=False)
        self.saved_locations_button.grid(row=0, column=1, padx=30, pady=10)

        self.settings_button_img = ctk.CTkImage(dark_image=Image.open("images/settings-icon-light.png"),
                                                light_image=Image.open("images/settings-icon-dark.png"),
                                                size=(195, 42))
        self.settings_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.settings_button_img,
                                             text="", command=lambda:view_control.show_frame(SettingsView),
                                             fg_color="transparent", hover=False)
        self.settings_button.grid(row=1, column=1, padx=30, pady=10)

        # Search Bar Frame
        self.search_bar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_bar_frame.grid(row=3, column=0, padx=30, pady=(50,30))

        self.label = ctk.CTkLabel(self.search_bar_frame, text='Enter a Location:')
        self.label.grid(row=1, column=0, padx=(0,5))

        self.location = ctk.StringVar()
        self.location_search = ctk.CTkEntry(self.search_bar_frame, textvariable=self.location, width=225)
        self.location_search.grid(row=1, column=1, padx=(7,10), sticky='e')

        self.location_search.insert(0, 'City Name, State/Country')
        self.location_search.bind("<FocusIn>", lambda y, w=self.location_search: self.on_entry_click(w))
        self.location_search.bind("<Return>", self.search_button_clicked)

        self.search_button = ctk.CTkButton(self.search_bar_frame, corner_radius=10, text='Search',
                                           command=self.search_button_clicked, fg_color="#5989d7",
                                           hover_color="#496fae")
        self.search_button.grid(row=1, column=2, padx=(20, 0), sticky='e')

        self.status_label = ctk.CTkLabel(self.search_bar_frame, text='')
        self.status_label.grid(row=1, column=1, sticky=ctk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def on_entry_click(self, widget):
        widget.delete(0, "end")  # delete all the text in the entry
        widget['foreground'] = 'black'

    def leave_entry(self, widget):
        widget.focus_set()

    # Begins the Search Logic upon clicking 'Search' or pressing enter
    def search_button_clicked(self):
        origin = 0

        if self.controller:
            self.controller.load(self.location.get(), origin)

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

        # Location Name Label
        self.location_label = ctk.CTkLabel(self, text="", font=("Arial", 20, "bold"))
        self.location_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, padx=0, pady=10, sticky="e")

        # Label of Weather Type
        self.weather_label = ctk.CTkLabel(self, text='')
        self.weather_label.grid(row=2, column=0, padx=40, pady=10, sticky="w")

        # Temperature (in degrees)
        self.temperature_label = ctk.CTkLabel(self, text='')
        self.temperature_label.grid(row=1, column=1, sticky="w")

        # Lowest Temperature for the Day
        self.temp_min_label = ctk.CTkLabel(self, text='')
        self.temp_min_label.grid(row=1, column=2, sticky="w")

        self.temp_min_value = ctk.CTkLabel(self, text='')
        self.temp_min_value.grid(row=4, column=0, sticky="w")

        self.temp_max_label = ctk.CTkLabel(self, text='')
        self.temp_max_label.grid(row=4, column=1, sticky="w")

        self.rain_label = ctk.CTkLabel(self, text='')
        self.rain_label.grid(row=4, column=2, sticky="w")

        self.wind_speed_label = ctk.CTkLabel(self, text='')
        self.wind_speed_label.grid(row=5, column=1, sticky="w")

        self.humidity_label = ctk.CTkLabel(self, text='')
        self.humidity_label.grid(row=5, column=2, sticky="w")

        self.sunrise_label = ctk.CTkLabel(self, text='')
        self.sunrise_label.grid(row=6, column=1, sticky="w")

        self.sunset_label = ctk.CTkLabel(self, text='')
        self.sunset_label.grid(row=6, column=2, sticky="w")

        """
        # Weather Data Frame
        self.info_widgets_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_widgets_frame.grid(row=0, column=0, stick='nsew')
        self.info_widgets_frame.columnconfigure(0, weight=1)
        self.info_widgets_frame.columnconfigure(1, weight=0)

        # Location Name Label
        self.location_label = ctk.CTkLabel(self.info_widgets_frame, text="", font=("Arial", 20, "bold"))
        self.location_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self.info_widgets_frame, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        
        # Label of Weather Type
        self.weather_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.weather_label.grid(row=2, column=0, padx=40, pady=10, sticky="w")

        # Temperature (in degrees)
        self.temperature_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temperature_label.grid(row=1, column=1, sticky="w")

        # Lowest Temperature for the Day
        self.temp_min_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_min_label.grid(row=1, column=2, sticky="w")

        self.temp_min_value = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_min_value.grid(row=4, column=0, sticky="w")

        self.temp_max_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.temp_max_label.grid(row=4, column=1, sticky="w")

        self.rain_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.rain_label.grid(row=4, column=2, sticky="w")

        self.wind_speed_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.wind_speed_label.grid(row=5, column=1, sticky="w")

        self.humidity_label= ctk.CTkLabel(self.info_widgets_frame, text='')
        self.humidity_label.grid(row=5, column=2, sticky="w")

        self.sunrise_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.sunrise_label.grid(row=6, column=1, sticky="w")

        self.sunset_label = ctk.CTkLabel(self.info_widgets_frame, text='')
        self.sunset_label.grid(row=6, column=2, sticky="w")

        """
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def set_location_name(self, location):
        self.location_label.configure(text=f"{location}")

    def set_weather(self, data):
        weather = data['weather'][0]['description']
        self.weather_label.configure(text=f"{weather}")

    def set_temperature(self, data):
        temperature = int(data['main']['temp'])
        self.temperature_label.configure(text=f"{temperature}")

    def set_temp_min(self, data):
        temp_min = int(data['main']['temp_min'])
        self.temp_min_label.configure(text=f"{temp_min}")

    def set_temp_max(self, data):
        temp_max = int(data['main']['temp_max'])
        self.temp_max_label.configure(text=f"{temp_max}")

    def set_rain(self, data):
        try:
            rain = data['rain']['1h']
        except KeyError:
            rain = "N/A"

        self.rain_label.configure(text=f"{rain}")

    def set_windSpeed(self, data):
        wind_speed = data['wind']['speed']
        self.wind_speed_label.configure(text=f"{wind_speed}")

    def set_humidity(self, data):
        humidity = data['main']['humidity']
        self.humidity_label.configure(text=f"{humidity}")

    def set_sunrise(self, data):
        sunrise = data['sys']['sunrise']

        convertedTime = datetime.fromtimestamp(sunrise)

        self.sunrise_label.configure(text=f"{convertedTime}")

    def set_sunset(self, data):
        sunset = data['sys']['sunset']

        convertedTime = datetime.fromtimestamp(sunset)

        self.sunset_label.configure(text=f"{convertedTime}")

    # def set_lastUpdate_time(self):

    def set_return_button(self, view_control, origin):
        if origin == 0:
            self.return_button.configure(text="Return to Home", command=lambda: view_control.show_frame(MainView))

        elif origin == 1:
            self.return_button.configure(text="Return to Saved Locations", command=lambda: view_control.show_frame(SavedView))

class SavedView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        self.frame_label = ctk.CTkLabel(self, text="Saved Locations", font=("Arial", 20, "bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        self.list_of_saved = ctk.CTkScrollableFrame(self, width=625, height=80)
        self.list_of_saved.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.controller = None
        self.pull_saved_locations()

    # Things to add/look into:
    # Hovering over location will show options to delete the location
    # Hovering over location will change its color
    # Clicking on location will open to StatsView for that location
    # Add feature to add new saved locations from the SavedView frame

    def set_controller(self, controller):
        self.controller = controller

    def pull_saved_locations(self):
        file_path = 'data/saved_locations.json'

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file {file_path}: {e}.")


        if len(data['saved_locations']) == 0:
            no_location_label = ctk.CTkLabel(self.list_of_saved, text="No Saved Locations.")
            no_location_label.grid(row=0, column=0, padx=40, pady=10, sticky='nsew')

        else:
            for i in range(len(data['saved_locations'])):
                location_text = data['saved_locations'][i]['location_name'] + ", " + data['saved_locations'][i]['country_name']

                location_label_frame = ctk.CTkFrame(self.list_of_saved, fg_color="transparent")
                location_label_frame.grid(row=i, column=0, padx=40, pady=5, sticky='w')

                location_label = ctk.CTkLabel(location_label_frame, text=f"{location_text}", font=("Arial", 15))
                location_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
                location_label.bind("<Enter>", lambda y, w=location_label: self.on_hover(w))
                location_label.bind("<Leave>", lambda y, w=location_label: self.on_leave(w))
                location_label.bind("<Button-1>", lambda y, w=location_label: self.on_select(w))


    def on_hover(self, label):
        label.configure(text_color="lightblue")

    def on_leave(self, label):
        label.configure(text_color="white")

    def on_select(self, label):
        origin = 1

        if self.controller:
            self.controller.load(label.cget("text"), origin)


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        self.view_c = view_control
        self.use_sys_mode = ctk.IntVar()
        self.night_mode = ctk.IntVar()
        self.temp_unit = ctk.StringVar()
        self.date_format = ctk.StringVar()
        self.time_format = ctk.StringVar()

        self.pull_setting_pref()

        # Label of the Frame
        self.frame_label = ctk.CTkLabel(self, text="Settings View", font=("Arial", 20, "bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="e")


        # 1) System/Manual Mode Toggle - Label
        self.mode_label = ctk.CTkLabel(self, text="Use System Default Mode", font=("Arial", 14))
        self.mode_label.grid(row=1, column=0, padx=(70, 20), pady=10, sticky="w")

        # 1) System/Manual Mode Toggle - Check Box
        self.mode_toggle = ctk.CTkCheckBox(self, text="", command=self.set_sys_mode, variable=self.use_sys_mode,
                                           onvalue=1, offvalue=0)
        self.mode_toggle.grid(row=1, column=1, padx=(10, 30), pady=20, sticky="w")

        # 2) Light/Dark Mode Toggle - Label
        self.toggle_label = ctk.CTkLabel(self, text="Theme Toggle", font=("Arial", 14))
        self.toggle_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # 2) Light/Dark Mode Toggle - Switch
        self.mode_switch = ctk.CTkSwitch(self, width=10, height=10, text="", command=self.set_dark_mode,
                                         variable=self.night_mode, onvalue=1, offvalue=0)
        self.mode_switch.grid(row=1, column=3, padx=(20, 50), pady=20, sticky="w")

        # 3) Temperature Units - Label
        self.temp_units_label = ctk.CTkLabel(self, text="Temperature Units", font=("Arial", 14))
        self.temp_units_label.grid(row=2, column=0, padx=15, pady=(30, 0), sticky="e")

        # 3) Temperature Units - Dropdown
        self.temp_units_list = ["Fahrenheit", "Celsius"]
        self.temp_units_menu = ctk.CTkOptionMenu(self, values=self.temp_units_list, command=self.set_temp_units,
                                                 variable=self.temp_unit)
        self.temp_units_menu.grid(row=3, column=0, padx=15, pady=15, sticky="e")

        # 4) Date Format - Label
        self.date_format_label = ctk.CTkLabel(self, text="Date Format", font=("Arial", 14))
        self.date_format_label.grid(row=2, column=1, padx=10, pady=(30, 0), sticky="w")

        # 4) Date Format - Dropdown
        self.date_format_list = ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY/MM/DD"]
        self.date_format_menu = ctk.CTkOptionMenu(self, values=self.date_format_list, command=self.set_date_format,
                                                 variable=self.date_format)
        self.date_format_menu.grid(row=3, column=1, padx=10, pady=15, sticky="w")

        # 5) Time Format - Label
        self.time_format_label = ctk.CTkLabel(self, text="Time Format", font=("Arial", 14))
        self.time_format_label.grid(row=2, column=2, padx=15, pady=(30, 0), sticky="w")

        # 5) Time Format - Dropdown
        self.time_format_list = ["12-Hour", "24-Hour"]
        self.time_format_menu = ctk.CTkOptionMenu(self, values=self.time_format_list, command=self.set_time_format,
                                                 variable=self.time_format)
        self.time_format_menu.grid(row=3, column=2, padx=15, pady=15, sticky="w")

        # Sets the saved settings
        self.set_widget_state()


    def pull_setting_pref(self):
        file_path = "data/settings.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            self.use_sys_mode.set(int(data['settings']['system_mode']))
            self.night_mode.set(int(data['settings']['night_mode']))
            self.temp_unit.set(data['settings']['temp_units'])
            self.date_format.set(data['settings']['date_format'])
            self.time_format.set(data['settings']['time_format'])

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

        self.set_temp_units(self.temp_unit)
        self.set_date_format(self.date_format)
        self.set_time_format(self.time_format)

    def set_sys_mode(self):
        self.view_c.show_frame(LoadView)

        if self.use_sys_mode.get() == 1:
            ctk.set_appearance_mode("System")
            self.update_json("system_mode", 1)
            self.mode_switch.configure(state="disabled")
            self.view_c.show_frame(SettingsView)

        elif self.use_sys_mode.get() == 0:
            self.mode_switch.configure(state="normal")
            self.update_json("system_mode", 0)
            self.set_dark_mode()

    def set_dark_mode(self):
        self.view_c.show_frame(LoadView)

        if self.night_mode.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.update_json("night_mode", self.night_mode.get())

        elif self.night_mode.get() == 0:
            ctk.set_appearance_mode("Light")
            self.update_json("night_mode", self.night_mode.get())

        self.view_c.show_frame(SettingsView)

    def set_temp_units(self, unit):
        self.update_json("temp_units", str(unit))

    def set_date_format(self, f):
        self.update_json("date_format", str(f))

    def set_time_format(self, f):
        self.update_json("time_format", str(f))

    def update_json(self, field, new_value):
        file_path = "data/settings.json"

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file {file_path}: {e}.")

        data['settings'][field] = new_value

        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

        except IOError as e:
            print(f"Error writing to {file_path}: {e}")
