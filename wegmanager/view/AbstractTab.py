import tkinter as tk
from abc import abstractmethod


class AbstractTab(tk.Frame):
    @abstractmethod
    def create_tab(self):
        raise NotImplementedError
