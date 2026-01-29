# The View defines the code for the display or features that the
# user interacts with.
import customtkinter as ctk
from datetime import datetime
from PIL import Image
import json

from numpy.ma.extras import row_stack

globalFont = "Helvetica"

class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, sticky="nsew")
        self.configure(width=700, height=200, fg_color="transparent")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Initializing frames to an empty array
        self.frames = {}

        # Iterating through a tuple consisting of
        # the different page layouts
        for F in (LoadView, MainView, StatsView, SettingsView, SavedView):
            frame = F(self, self)

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

        # Centers main_menu_frame and search_bar_frame on the parent frame
        self.columnconfigure(0, weight=1)
        self.bind("<Button-1>", lambda y, w=self: self.leave_entry(w))

        """ Main Menu Options Frame """
        self.main_menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_menu_frame.grid(row=0, column=0, sticky='nsew', padx=30, pady=20)
        self.main_menu_frame.grid_columnconfigure(0, weight=1)
        #self.main_menu_frame.bind("<Button-1>", lambda y, w=self.main_menu_frame: self.leave_entry(w))

        self.main_icon_img = ctk.CTkImage(light_image=Image.open("images/main-app-icon.png"), size=(280, 145))
        self.main_icon = ctk.CTkLabel(self.main_menu_frame, image=self.main_icon_img, text="")
        self.main_icon.grid(row=0, column=0, rowspan=2, padx=30, pady=10, sticky="nsew")

        self.saved_locations_button_img = ctk.CTkImage(dark_image=Image.open("images/saved-locations-dark.png"),
                                                       light_image=Image.open("images/saved-locations-light.png"),
                                                       size=(205, 45))
        self.saved_locations_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.saved_locations_button_img,
                                                    text="", command=lambda:view_control.show_frame(SavedView),
                                                    fg_color="transparent", hover=False)
        self.saved_locations_button.grid(row=0, column=1, padx=30, pady=10)

        self.settings_button_img = ctk.CTkImage(dark_image=Image.open("images/settings-dark.png"),
                                                light_image=Image.open("images/settings-light.png"),
                                                size=(205, 45))
        self.settings_button = ctk.CTkButton(self.main_menu_frame, corner_radius=10, image=self.settings_button_img,
                                             text="", command=lambda:view_control.show_frame(SettingsView),
                                             fg_color="transparent", hover=False)
        self.settings_button.grid(row=1, column=1, padx=30, pady=10)

        # Search Bar Frame
        self.search_bar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_bar_frame.grid(row=2, column=0, padx=30, pady=50)

        self.label = ctk.CTkLabel(self.search_bar_frame, text='Enter a Location:', font=("Arial", 15, "bold"))
        self.label.grid(row=1, column=0, padx=(0,5))

        self.location = ctk.StringVar()
        self.location_search = ctk.CTkEntry(self.search_bar_frame, textvariable=self.location, width=250, font=("Arial", 13))
        self.location_search.grid(row=1, column=1, padx=(7,10), sticky='e')

        self.location_search.insert(0, 'City Name, State/Country')
        self.location_search.bind("<FocusIn>", lambda y, w=self.location_search: self.on_entry_click(w))
        self.location_search.bind("<Return>", self.search_button_clicked)

        self.search_button = ctk.CTkButton(self.search_bar_frame, corner_radius=10, text='Search', font=("Arial", 15, "bold"),
                                           command=self.search_button_clicked, fg_color="#5989d7",
                                           hover_color="#496fae")
        self.search_button.grid(row=1, column=2, padx=(20, 0), sticky='e')

        self.status_label = ctk.CTkLabel(self.search_bar_frame, text='')
        self.status_label.grid(row=1, column=1, sticky=ctk.W)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def on_entry_click(self, widget):
        if self.location.get() == "City Name, State/Country":
            widget.delete(0, "end")  # delete all the text in the entry
            widget['foreground'] = 'black'

    def leave_entry(self, widget):
        widget.focus_set()

        if self.location.get() == "":
            self.location_search.insert(0, 'City Name, State/Country')

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

        self.configure(fg_color="transparent")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        """ Icon Frame """
        self.icon_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.icon_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.icon_frame.rowconfigure(0, weight=1)

        # Weather Type Icon
        self.weather_icon_path = ctk.StringVar()
        self.weather_icon_img = ctk.CTkImage(light_image=Image.open("images/sunny-icon.png"), size=(175, 175))
        self.weather_icon = ctk.CTkLabel(self.icon_frame, image=self.weather_icon_img, text="")
        self.weather_icon.grid(row=0, column=0, rowspan=2, padx=20, pady=10, sticky="nsew")

        """ Top Row Frame """
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=1, sticky="nsew")
        self.top_frame.columnconfigure(0, weight=1)

        # Location Name Label
        self.location_label = ctk.CTkLabel(self.top_frame, text="", font=("Arial", 30, "bold"))
        self.location_label.grid(row=0, column=0, columnspan=3, padx=(0,20), pady=(40,10), sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self.top_frame, corner_radius=10, text='Return to Home',
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, padx=(10,20), pady=(40,10), sticky="e")


        # Bottom Row Frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=1, sticky="nsew")

        """ Bottom Column 0 """
        self.bottom_col_0 = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.bottom_col_0.grid(row=0, column=0, sticky="nsew")

        # Temperature (degrees F or C)
        self.current_temp_value = ctk.CTkLabel(self.bottom_col_0, text='', font=("Arial", 80))
        self.current_temp_value.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Weather Type Description
        self.weather_label = ctk.CTkLabel(self.bottom_col_0, text='')
        self.weather_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        """ Bottom Column 1 """
        self.bottom_col_1 = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.bottom_col_1.grid(row=0, column=1, sticky="nsew")

        # Max Temperature (degrees F or C)
        self.temp_max_label = ctk.CTkLabel(self.bottom_col_1, text='Max')
        self.temp_max_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.temp_max_value = ctk.CTkLabel(self.bottom_col_1, text='')
        self.temp_max_value.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Min Temperature (degrees F or C)
        self.temp_min_label = ctk.CTkLabel(self.bottom_col_1, text='Min')
        self.temp_min_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        self.temp_min_value = ctk.CTkLabel(self.bottom_col_1, text='')
        self.temp_min_value.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        # Feels Like Temperature (degrees F or C)
        self.feels_like_temp_label = ctk.CTkLabel(self.bottom_col_1, text='Feels Like')
        self.feels_like_temp_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.feels_like_temp = ctk.CTkLabel(self.bottom_col_1, text='')
        self.feels_like_temp.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        """ Bottom Column 2 """
        self.bottom_col_2 = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.bottom_col_2.grid(row=0, column=2, sticky="nsew")

        # Amount of Rain or Snow (mm/h)
        self.precipitation_label = ctk.CTkLabel(self.bottom_col_2, text='Rain')
        self.precipitation_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.precipitation_value = ctk.CTkLabel(self.bottom_col_2, text='')
        self.precipitation_value.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Humidity (%)
        self.humidity_label = ctk.CTkLabel(self.bottom_col_2, text='Humidity')
        self.humidity_label.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        self.humidity_value = ctk.CTkLabel(self.bottom_col_2, text='')
        self.humidity_value.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        # Wind_speed (L/T)
        self.wind_speed_label = ctk.CTkLabel(self.bottom_col_2, text='Wind Speed')
        self.wind_speed_label.grid(row=4, column=3, padx=10, pady=10, sticky="w")

        self.wind_speed_value = ctk.CTkLabel(self.bottom_col_2, text='')
        self.wind_speed_value.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        """ Bottom Column 3 """
        self.bottom_col_3 = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.bottom_col_3.grid(row=0, column=3, sticky="nsew")

        # Sunrise Time
        self.sunrise_label = ctk.CTkLabel(self.bottom_col_3, text='Sunrise')
        self.sunrise_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        self.sunrise_value = ctk.CTkLabel(self.bottom_col_3, text='')
        self.sunrise_value.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        # Sunset Time
        self.sunset_label = ctk.CTkLabel(self.bottom_col_3, text='Sunset')
        self.sunset_label.grid(row=2, column=4, padx=10, pady=10, sticky="w")

        self.sunset_value = ctk.CTkLabel(self.bottom_col_3, text='')
        self.sunset_value.grid(row=3, column=4, padx=10, pady=10, sticky="w")

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def set_location_name(self, location):
        self.location_label.configure(text=f"{location}")

    def set_weather(self, data):
        weather = data['weather'][0]['description']
        self.weather_label.configure(text=f"{weather}")

    def set_temperature(self, data):
        temperature = str(int(data['main']['temp'])) + "°"
        self.current_temp_value.configure(text=f"{temperature}")

    def set_temp_min(self, data):
        temp_min = str(int(data['main']['temp_min'])) + "°"
        self.temp_min_value.configure(text=f"{temp_min}")

    def set_temp_max(self, data):
        temp_max = str(int(data['main']['temp_max'])) + "°"
        self.temp_max_value.configure(text=f"{temp_max}")

    def set_feels_like_temp(self, data):
        feels_like_temp = str(int(data['main']['feels_like'])) + "°"
        self.feels_like_temp.configure(text=f"{feels_like_temp}")

    def set_precipitation(self, data):
        try:
            precipitation = data['rain']['1h']
        except KeyError:
            precipitation = "0"

        self.precipitation_value.configure(text=f"{precipitation}")

    def set_wind_speed(self, data):
        wind_speed = data['wind']['speed']
        self.wind_speed_value.configure(text=f"{wind_speed}")

    def set_humidity(self, data):
        humidity = data['main']['humidity']
        self.humidity_value.configure(text=f"{humidity}")

    def set_sunrise(self, data):
        sunrise = data['sys']['sunrise']

        convertedTime = datetime.fromtimestamp(sunrise)

        self.sunrise_value.configure(text=f"{convertedTime}")

    def set_sunset(self, data):
        sunset = data['sys']['sunset']

        convertedTime = datetime.fromtimestamp(sunset)

        self.sunset_value.configure(text=f"{convertedTime}")

    # def set_lastUpdate_time(self):

    def set_return_button(self, view_control, origin):
        if origin == 0:
            self.return_button.configure(text="Return to Home", command=lambda: view_control.show_frame(MainView))

        elif origin == 1:
            self.return_button.configure(text="Return to Saved Locations", command=lambda: view_control.show_frame(SavedView))

class SavedView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        self.columnconfigure(0, weight=1)

        self.frame_label = ctk.CTkLabel(self, text="Saved Locations", font=("Arial", 26, "bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self, corner_radius=10, text='Return to Home', font=("Arial", 15, "bold"),
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="e")

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
        label.configure(text_color="#5d86c7")

    def on_leave(self, label):
        label.configure(text_color="white")

    def on_select(self, label):
        origin = 1

        if self.controller:
            self.controller.load(label.cget("text"), origin)


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, view_control):
        ctk.CTkFrame.__init__(self, parent)

        self.columnconfigure(0, weight=1)

        self.view_c = view_control
        self.use_sys_mode = ctk.IntVar()
        self.night_mode = ctk.IntVar()
        self.temp_unit = ctk.StringVar()
        self.unit_sys = ctk.StringVar()
        self.date_format = ctk.StringVar()
        self.time_format = ctk.StringVar()

        self.pull_setting_pref()

        # Top Row Frame
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.columnconfigure(0, weight=1)

        # Label of the Frame
        self.frame_label = ctk.CTkLabel(self.top_frame, text="Settings", font=("Arial", 26, "bold"))
        self.frame_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Return to Home Button
        self.return_button = ctk.CTkButton(self.top_frame, corner_radius=10, text='Return to Home', font=("Arial", 15, "bold"),
                                           command=lambda: view_control.show_frame(MainView), fg_color="#5989d7",
                                           hover_color="#496fae")
        self.return_button.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="e")

        # Middle Row Frame
        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.grid(row=1, column=0, sticky="nsew")
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.columnconfigure(1, weight=1)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=1)

        # 1) System/Manual Mode Toggle - Label
        self.mode_label = ctk.CTkLabel(self.middle_frame, text="Use System Default Theme", font=("Arial", 14))
        self.mode_label.grid(row=1, column=0, padx=(70, 0), pady=10, sticky="w")

        # 1) System/Manual Mode Toggle - Check Box
        self.mode_toggle = ctk.CTkCheckBox(self.middle_frame, text="", command=self.set_sys_mode, variable=self.use_sys_mode,
                                           onvalue=1, offvalue=0)
        self.mode_toggle.grid(row=1, column=1, padx=(0,10), pady=20, sticky="w")

        # 2) Light/Dark Mode Toggle - Label
        self.toggle_label = ctk.CTkLabel(self.middle_frame, text="Theme Toggle", font=("Arial", 14))
        self.toggle_label.grid(row=1, column=2, padx=(5, 0), pady=10, sticky="w")

        # 2) Light/Dark Mode Toggle - Switch
        self.mode_switch = ctk.CTkSwitch(self.middle_frame, width=5, height=10, text="", command=self.set_dark_mode,
                                         variable=self.night_mode, onvalue=1, offvalue=0)
        self.mode_switch.grid(row=1, column=3, padx=(0, 40), pady=20, sticky="w")

        # Bottom Row Frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)
        self.bottom_frame.columnconfigure(3, weight=1)

        # 3) Temperature Units - Label
        self.temp_units_label = ctk.CTkLabel(self.bottom_frame, text="Temperature Units", font=("Arial", 14))
        self.temp_units_label.grid(row=2, column=0, padx=(30, 0), pady=(30, 0), sticky="nsew")

        # 3) Temperature Units - Dropdown
        self.temp_units_list = ["Fahrenheit", "Celsius"]
        self.temp_units_menu = ctk.CTkOptionMenu(self.bottom_frame, width=130, values=self.temp_units_list,
                                                 command=self.set_temp_units, variable=self.temp_unit, dynamic_resizing=False)
        self.temp_units_menu.grid(row=3, column=0, padx=(30, 0), pady=15)

        # 4) Unit System - Label
        self.temp_units_label = ctk.CTkLabel(self.bottom_frame, text="Unit System", font=("Arial", 14))
        self.temp_units_label.grid(row=2, column=1, padx=0, pady=(30, 0), sticky="nsew")

        # 4) Unit System - Dropdown
        self.unit_sys_list = ["Imperial", "Metric"]
        self.temp_units_menu = ctk.CTkOptionMenu(self.bottom_frame, width=130, values=self.unit_sys_list,
                                                 command=self.set_unit_sys_type, variable=self.unit_sys, dynamic_resizing=False)
        self.temp_units_menu.grid(row=3, column=1, padx=0, pady=15)

        # 5) Date Format - Label
        self.date_format_label = ctk.CTkLabel(self.bottom_frame, text="Date Format", font=("Arial", 14))
        self.date_format_label.grid(row=2, column=2, padx=0, pady=(30, 0), sticky="nsew")

        # 5) Date Format - Dropdown
        self.date_format_list = ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY/MM/DD"]
        self.date_format_menu = ctk.CTkOptionMenu(self.bottom_frame, width=130, values=self.date_format_list,
                                                  command=self.set_date_format, variable=self.date_format, dynamic_resizing=False)
        self.date_format_menu.grid(row=3, column=2, padx=0, pady=15)

        # 6) Time Format - Label
        self.time_format_label = ctk.CTkLabel(self.bottom_frame, text="Time Format", font=("Arial", 14))
        self.time_format_label.grid(row=2, column=3, padx=(0,30), pady=(30, 0), sticky="nsew")

        # 6) Time Format - Dropdown
        self.time_format_list = ["12-Hour", "24-Hour"]
        self.time_format_menu = ctk.CTkOptionMenu(self.bottom_frame, width=130, values=self.time_format_list,
                                                  command=self.set_time_format, variable=self.time_format, dynamic_resizing=False)
        self.time_format_menu.grid(row=3, column=3, padx=(0,30), pady=15)

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
            self.unit_sys.set(data['settings']['unit_sys'])
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

    def set_temp_units(self, u):
        self.update_json("temp_units", str(u))

    def set_unit_sys_type(self, t):
        self.update_json("unit_sys", str(t))

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
