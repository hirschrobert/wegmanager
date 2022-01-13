from view.AbstractTab import AbstractTab
import tkinter as tk
from tkinter import ttk


class Form(AbstractTab):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.entries = {}
        self.buttons = {}
        self.comboboxes = {}
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

    def create_view(self, neighbourhoods: list, room_type: list):

        control_frame = tk.LabelFrame(master=self, text="Input data")
        control_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(0, weight=1)
        control_frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.create_combobox(
            control_frame, "Neighbourhood", row=0, column=0, values=neighbourhoods
        )
        self.create_combobox(
            control_frame, "Room type", row=0, column=1, values=room_type
        )

        self.create_entry(
            control_frame, "Minimum night", row=1, column=0, textvar=tk.DoubleVar()
        )
        self.create_entry(
            control_frame, "Guests", row=1, column=1, textvar=tk.DoubleVar()
        )

        self.create_entry(
            control_frame, "Bedrooms", row=2, column=0, textvar=tk.DoubleVar()
        )
        self.create_entry(
            control_frame, "Beds", row=2, column=1, textvar=tk.DoubleVar()
        )

        self.create_entry(
            control_frame, "Bath rooms", row=2, column=2, textvar=tk.DoubleVar()
        )

        self.create_button(control_frame, "Valider", row=3, column=0)

    def create_entry(self, frame, label, row, column, textvar):
        label_frame = tk.LabelFrame(frame, text=label)
        self.entries[label] = tk.Entry(label_frame, textvariable=textvar)
        self.entries[label].grid(row=1, column=1)
        label_frame.grid(row=row, column=column,
                         sticky=tk.N + tk.S + tk.E + tk.W)

    def create_button(self, frame, name, row, column):
        self.buttons[name] = tk.Button(frame)
        self.buttons[name]["text"] = name
        self.buttons[name].grid(row=row, column=column)

    def create_combobox(self, frame, label, values, row, column):
        label_frame = tk.LabelFrame(frame, text=label)
        self.comboboxes[label] = ttk.Combobox(label_frame, values=values)
        self.comboboxes[label].grid(row=1, column=1)
        label_frame.grid(row=row, column=column,
                         sticky=tk.N + tk.S + tk.E + tk.W)
