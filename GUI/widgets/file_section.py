from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar

from GUI.utils.core import WidgetHelpers


class FileSectionParent(QWidget):

    def __init__(self, section_label: str, action_button_label: str, select_input_dir_handler: Callable, select_output_dir_handler: Callable, action_btn_handler: Callable, additional_layouts: list = None, **kwargs):
        if not section_label or not action_button_label:
            raise FileSectionError("Section Label and Action Button Label ")
        if not select_input_dir_handler or not select_output_dir_handler:
            raise FileSectionError("Both, select input and output handlers, are required.")

        super().__init__()
        self.file_section_layout = QVBoxLayout()
        self.section_label = section_label
        self.action_btn_label = action_button_label
        self.select_input_dir_handler = select_input_dir_handler
        self.select_output_dir_handler = select_output_dir_handler
        self.action_btn_handler = action_btn_handler
        self.additional_layouts = additional_layouts
        self.file_section_group = None
        self.input_dir_label = None
        self.select_input_dir_button = None
        self.output_dir_label = None
        self.select_output_dir_button = None
        self.progress_bar = None

    def render_ui(self):
        self.file_section_group = QGroupBox(self.section_label)
        self.build_main_input_output_subsection()
        self.generate_additional_layouts()
        self.generate_action_btn_layout()

    def build_main_input_output_subsection(self):
        self.file_section_layout.addLayout(
            self.generate_select_file_section('Input Directory: Not Selected', 'Select Input Directory', self.select_input_dir_handler)
        )
        self.file_section_layout.addLayout(
            self.generate_select_file_section('Output Directory: Not Selected', 'Select Output Directory', self.select_output_dir_handler)
        )

    def generate_action_btn_layout(self):
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addWidget(
            WidgetHelpers.configure_widget(widget=QPushButton(self.action_btn_label), min_width=170, max_width=180, click_handler=self.action_btn_handler)
        )
        action_btn_layout.addWidget(
            WidgetHelpers.configure_widget(widget=QLabel("Waiting to process files..."), set_visible=False, word_wrap=True)
        )
        self.progress_bar = WidgetHelpers.configure_widget(widget=QProgressBar(self), set_minimum=0, set_value=0, set_visible=False)
        action_btn_layout.setAlignment(Qt.AlignCenter)
        self.file_section_layout.addLayout(action_btn_layout)

    def generate_additional_layouts(self):
        if self.additional_layouts is not None:
            for layout in self.additional_layouts:
                self.file_section_layout.addLayout(layout)

    @staticmethod
    def generate_select_file_section(dir_label_str: str, select_dir_btn: str, btn_event: Callable) -> QHBoxLayout:
        directory_layout = QHBoxLayout()
        directory_label = WidgetHelpers.configure_widget(widget=QLabel(dir_label_str), word_wrap=True, min_width=200, max_width=300)
        select_input_dir_button = WidgetHelpers.configure_widget(widget=QPushButton(select_dir_btn), min_width=170, max_width=180, click_handler=btn_event)
        directory_layout.addWidget(directory_label)
        directory_layout.addWidget(select_input_dir_button)
        return directory_layout


class FileSectionError(Exception):
    def __init__(self, message):
        super().__init__(message)
