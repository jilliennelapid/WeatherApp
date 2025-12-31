from model import Model
from view import View, StatsView, SettingsView, SavedView

from controller import Controller
from dotenv import load_dotenv
import customtkinter as ctk
import os


def configure():
    load_dotenv()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        api_key = os.getenv('APIkey')

        model = Model(api_key)
        view = View(self)
        controller = Controller(model, view)

        view.grid(row=0, column=0, padx=10, pady=10)
        self.resizable(False, False)

        View.set_controller(view, controller)
        Controller.set_frames(controller, view)


if __name__ == '__main__':
    configure()
    # Creates an object from class App, which also creates the window using tkinter module
    app = App()
    app.mainloop()
