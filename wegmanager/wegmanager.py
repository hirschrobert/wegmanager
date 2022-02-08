#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point of the app.
"""
from os import path
import sys
import signal

from tkinter import Image, Tk
from wegmanager.controller.application import Application


def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN)  # ignore additional signals
    # cleanup() # give your process a chance to clean up
    sys.exit(0)


def main() -> Tk:
    """ Main function defining app properties."""

    appname = "WEG Manager"
    window = Tk(className=appname)
    window.wm_title(appname)
    signal.signal(signal.SIGINT, signal_handler)

    # Adjust size
    window_width = 1000
    window_height = 800

    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # window.geometry("800x600")

    # set minimum window size value
    window.minsize(window_width, window_height)

    # Icon
    # source: https://www.flaticon.com/free-icon/assets_1907675
    # credit: https://www.flaticon.com/authors/ddara
    # get icon
    # Get the absolute path of this file
    path_to_icon = path.abspath(path.join(path.dirname(__file__), 'icon.png'))

    img = Image("photo", file=path_to_icon)
    window.iconphoto(True, img)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.withdraw()
    window.after(0, window.deiconify)
    app_path = path.abspath(path.dirname(__file__))
    _app = Application(parent=window, app_path=app_path)


if __name__ == '__main__':
    sys.exit(main())
