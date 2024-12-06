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

    def refresh_window(self) -> None:
        self.repaint()
        self.update()
        QApplication.processEvents()

    # def make_file_processor_tab(self):
    #     # TODO this could potentially be made into it's own class later
    #     main_tab = QWidget()
    #     self.main_layout = QVBoxLayout(main_tab)
    #
    #     logo_layout = QHBoxLayout()
    #     logo_layout.setAlignment(Qt.AlignCenter)
    #     self.create_logo(logo_layout)
    #     self.main_layout.addLayout(logo_layout)
    #
    #     # Input directory layout
    #     self.random_name_section = QHBoxLayout()
    #     self.random_name_label = QLabel("Click the button to update this text")
    #     self.random_name_label.setAlignment(Qt.AlignCenter)
    #     self.random_name_label.setObjectName("RandomNameLabelEmpty")
    #
    #     # Create the button
    #     self.random_name_button = QPushButton("Generate Name")
    #     self.random_name_button.setObjectName("RandomNameButton")
    #     self.random_name_button.clicked.connect(self.update_random_name_label)
    #
    #     # Add label and button to the layout
    #     self.random_name_section.addWidget(self.random_name_label)
    #     self.random_name_section.addWidget(self.random_name_button)
    #
    #     self.main_layout.addLayout(self.random_name_section)
    #
    #     # Output directory layout
    #     self.build_input_output_dir_section()
    #
    #     # Add main tab
    #     self.tab_widget.addTab(main_tab, "Main")
    #
    # def create_logo(self, logo_layout) -> None:
    #     logo_label = QLabel(self)
    #     pixmap = QPixmap(LEMON_CABLE_APP_LOGO_PATH)
    #
    #     if pixmap.isNull():
    #         print(f"Failed to load image: {LEMON_CABLE_APP_LOGO_PATH}")
    #         logo_label.setText("Logo failed to load.")
    #     else:
    #         scaled_pixmap = pixmap.scaled(500, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #         logo_label.setPixmap(scaled_pixmap)
    #
    #     logo_label.setAlignment(Qt.AlignCenter)
    #     logo_label.setObjectName("logo_label")
    #     logo_label.setMinimumSize(500, 250)
    #
    #     logo_layout.addWidget(logo_label)

    # def update_random_name_label(self):
    #     print("Button clicked yo")
    #     """Update the label text and apply a new style."""
    #     self.random_name_label.setText(self.namer.generate_title())
    #     self.random_name_label.setObjectName('RandomNameLabelWithName')
    #
    # def build_input_output_dir_section(self):
    #     input_dir_layout = QHBoxLayout()
    #     self.input_dir_label = QLabel("Input Directory: Not Selected")
    #     self.input_dir_label.setWordWrap(True)  # Allow text wrapping to a new line
    #     self.input_dir_label.setMinimumWidth(200)
    #     self.input_dir_label.setMaximumWidth(300)
    #     self.select_input_button = QPushButton("Select Input Directory")
    #     self.select_input_button.setMinimumWidth(170)
    #     self.select_input_button.setMaximumWidth(180)
    #     self.select_input_button.clicked.connect(self.select_input_directory)
    #
    #     input_dir_layout.addWidget(self.input_dir_label)
    #     input_dir_layout.addWidget(self.select_input_button)
    #     self.main_layout.addLayout(input_dir_layout)
    #
    #     output_dir_layout = QHBoxLayout()
    #     self.output_dir_label = QLabel("Output Directory: Not Selected")
    #     self.output_dir_label.setWordWrap(True)  # Allow text wrapping to a new line
    #     self.output_dir_label.setMinimumWidth(200)
    #     self.output_dir_label.setMaximumWidth(300)
    #     self.select_output_button = QPushButton("Select Output Directory")
    #     self.select_output_button.setMinimumWidth(170)
    #     self.select_output_button.setMaximumWidth(180)
    #     self.select_output_button.clicked.connect(self.select_output_directory)
    #     output_dir_layout.addWidget(self.output_dir_label)
    #     output_dir_layout.addWidget(self.select_output_button)
    #     self.main_layout.addLayout(output_dir_layout)
    #
    # # TODO move this shit to the controller class
    # def select_input_directory(self):
    #     dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
    #     if dir_path:
    #         self.input_dir = dir_path
    #         self.input_dir_label.setText(f"Input Directory: {dir_path}")
    #
    # def select_output_directory(self):
    #     dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
    #     if dir_path:
    #         self.output_dir = dir_path
    #         self.output_dir_label.setText(f"Output Directory: {dir_path}")
    #
    # def clean_music(self):
    #     # TODO This should be moved to liek a file processor  class and have this method call the method of that class.
    #     if not self.input_dir or not self.output_dir:
    #         QMessageBox.warning(self, "Error", "Please select both input and output directories.")
    #         return
    #
    #     # Process each file in the input directory
    #     for index, filename in enumerate(os.listdir(self.input_dir)):
    #         file_path = os.path.join(self.input_dir, filename)
    #         if not os.path.isfile(file_path):
    #             continue
    #
    #         try:
    #             # Load audio
    #             audio = AudioSegment.from_file(file_path)
    #
    #             # Detect nonsilent parts
    #             nonsilent_ranges = detect_nonsilent(audio, min_silence_len=2000, silence_thresh=-40)
    #
    #             # Combine nonsilent parts
    #             trimmed_audio = AudioSegment.empty()
    #             for start, end in nonsilent_ranges:
    #                 trimmed_audio += audio[start:end]
    #
    #             # Save to output directory with modified filename
    #             original_name, ext = os.path.splitext(filename)
    #             new_name = f"{original_name}_processed_{index}{ext}"
    #             output_path = os.path.join(self.output_dir, new_name)
    #             trimmed_audio.export(output_path, format=ext.lstrip('.'))
    #         except Exception as e:
    #             QMessageBox.warning(self, "Error", f"Error processing {filename}: {e}")
    #
    #     QMessageBox.information(self, "Success", "Music files processed successfully!")
