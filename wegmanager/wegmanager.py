"""
Main entry point of the app.
"""
from __future__ import absolute_import
from tkinter import Image, Tk
from wegmanager.controller.Application import Application
from os import path
import sys


def main() -> None:
    appname = "WEG Manager"
    # TODO: className shows title in first letter upper case rest lower case,
    # probably a real class name rather than a string
    window = Tk(className=appname)
    window.wm_title(appname)
    # Adjust size
    window.geometry("800x600")

    # set minimum window size value
    window.minsize(800, 600)

    # set maximum window size value
    #window.maxsize(800, 600)

    # Icon
    # source: https://www.flaticon.com/free-icon/assets_1907675
    # credit: https://www.flaticon.com/authors/ddara
    # get icon
    try:
        # Get the absolute path of the temp directory
        path_to_icon = path.abspath(
            path.join(path.dirname(__file__), 'icon.png'))
        img = Image("photo", file=path_to_icon)
        window.tk.call('wm', 'iconphoto', window._w, img)
    except:
        pass

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    app = Application(parent=window)


if __name__ == '__main__':
    sys.exit(main())
