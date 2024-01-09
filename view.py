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