#!/usr/bin/env python
"""
Main entry point of the app.
"""
from os import path
import sys

from tkinter import Image, Tk
from wegmanager.controller.application import Application


def main() -> Tk:

    """ Main function defining app properties."""

    appname = "WEG Manager"
    # TODO: className shows title in first letter upper case rest lower case,
    # probably a real class name rather than a string
    window = Tk(className=appname)
    window.wm_title(appname)
    # Adjust size
    window.geometry("800x600")

    # set minimum window size value
    window.minsize(800, 600)

    # Icon
    # source: https://www.flaticon.com/free-icon/assets_1907675
    # credit: https://www.flaticon.com/authors/ddara
    # get icon
    # Get the absolute path of the temp directory
    path_to_icon = path.abspath(path.join(path.dirname(__file__), 'icon.png'))
    img = Image("photo", file=path_to_icon)
    window.iconphoto(True, img)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    _app = Application(parent=window)


if __name__ == '__main__':
    sys.exit(main())
