import os
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout, QFileDialog, QTabWidget

from pydub import AudioSegment
from pydub.silence import detect_nonsilent

from GUI.tabs.home import HomeUI
from GUI.tabs.step_form import StepForm
from controllers.name_generator import NameGenerator
from webdriver.controller import WebDriverController

# lets make the gui open the stylesheet
STYLESHEET_PATH = os.path.join("GUI", "styles.qss")


class LemonCableGUI(QWidget):
    """Main GUI class with tabbed interface."""

    def __init__(self, webdriver_controller: WebDriverController):
        super().__init__()
        self.input_dir = None
        self.output_dir = None
        self.random_name_label = None
        self.random_name_button = None
        self.random_name_section = None
        self.select_output_button = None
        self.select_input_button = None
        self.input_dir_label = None
        self.output_dir_label = None
        self.app_layout = None
        self.main_layout = None
        self.webdriver_controller = webdriver_controller

        self.setWindowTitle("LemonCable")
        self.setGeometry(200, 200, 600, 400)

        # Create a tab widget
        self.tab_widget = QTabWidget()
        self.init_tabs()

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def init_tabs(self):
        # Wrap main layout in a QWidget
        # self.make_file_processor_tab()

        # Tab 2: WebDriver Control
        webdriver_tab = QWidget()
        webdriver_layout = QVBoxLayout(webdriver_tab)

        start_button = QPushButton("Start WebDriver")
        stop_button = QPushButton("Stop WebDriver")

        start_button.clicked.connect(
            lambda: threading.Thread(target=self.webdriver_controller.start_driver, daemon=True).start()
        )
        stop_button.clicked.connect(self.webdriver_controller.stop_driver)

        webdriver_layout.addWidget(QLabel("Control WebDriver:"))
        webdriver_layout.addWidget(start_button)
        webdriver_layout.addWidget(stop_button)

        home_tab = HomeUI()
        self.tab_widget.addTab(home_tab, "Albums")

        # Tab 3: Step Form
        step_form_tab = StepForm(self.webdriver_controller)
        self.tab_widget.addTab(step_form_tab, "Step Manager")

        self.tab_widget.addTab(webdriver_tab, "Web Driver")
        self.refresh_window()

    def refresh_window(self) -> None:
        self.repaint()
        self.update()
        QApplication.processEvents()
