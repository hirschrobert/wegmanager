"""
Main entry point of the app.
"""
from tkinter import Image, Tk
from controller.Application import Application

if __name__ == "__main__":
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
    img = Image("photo", file="icon.png")
    window.tk.call('wm', 'iconphoto', window._w, img)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    app = Application(parent=window)
