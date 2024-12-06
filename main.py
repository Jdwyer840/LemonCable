# This is a sample Python script.
import os
import sys

from PyQt5.QtWidgets import QApplication

from GUI.lemon_cable import LemonCableGUI
from webdriver.controller import WebDriverController


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller temp directory
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.getcwd(), relative_path)
ffmpeg_path = resource_path('resources/ffmpeg/bin/ffmpeg.exe')
ffprobe_path = resource_path('resources/ffmpeg/bin/ffprobe.exe')
os.environ["FFMPEG_BINARY"] = ffmpeg_path
os.environ["FFPROBE_BINARY"] = ffprobe_path
if __name__ == "__main__":
    app = QApplication([])

    # Load the external stylesheet
    stylesheet_path = resource_path("GUI/static/styles.qss")
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())
    else:
        print(f"Stylesheet not found at: {stylesheet_path}")

    # Initialize the WebDriver and GUI
    webdriver = WebDriverController()
    window = LemonCableGUI(webdriver_controller=webdriver)
    window.show()
    app.exec_()
