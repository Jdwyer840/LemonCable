from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QFileDialog

from GUI.utils.core import WidgetHelpers


class FileSectionParent(QWidget):

    def __init__(self, section_label: str, action_button_label: str, action_btn_handler: Callable, additional_layouts: list = None, **kwargs):
        self.output_dir = None
        self.input_dir = None
        self.action_btn = None
        if not section_label or not action_button_label:
            raise FileSectionError("Section Label and Action Button Label ")

        super().__init__()
        self.layout = QVBoxLayout()
        self.file_section_layout = QVBoxLayout()
        self.section_label = section_label
        self.action_btn_label = action_button_label
        # self.select_input_dir_handler = select_input_dir_handler
        # self.select_output_dir_handler = select_output_dir_handler
        self.action_btn_handler = action_btn_handler
        self.additional_layouts = additional_layouts
        self.file_section_group = None
        self.input_dir_label = None
        self.select_input_dir_button = None
        self.output_dir_label = None
        self.select_output_dir_button = None
        self.progress_bar = None
        self.progress_label = None
        self.render_ui()

    def render_ui(self):
        self.file_section_group = QGroupBox(self.section_label)
        self.build_main_input_output_subsection()
        self.generate_additional_layouts()
        self.generate_action_btn_layout()
        self.file_section_group.setLayout(self.file_section_layout)
        self.layout.addWidget(self.file_section_group)
        self.setLayout(self.layout)

    def build_main_input_output_subsection(self):
        input_dir_layout = QHBoxLayout()
        self.input_dir_label = WidgetHelpers.configure_widget(widget=QLabel('Input Directory: Not Selected'), word_wrap=True, min_width=200, max_width=300)
        self.select_input_dir_button = WidgetHelpers.configure_widget(widget=QPushButton('Select Input Directory'), min_width=170, max_width=180, click_handler=self.select_input_directory)
        input_dir_layout.addWidget(self.input_dir_label)
        input_dir_layout.addWidget(self.select_input_dir_button)
        self.file_section_layout.addLayout(
            input_dir_layout
        )

        output_dir_layout = QHBoxLayout()
        self.output_dir_label = WidgetHelpers.configure_widget(widget=QLabel('Output Directory: Not Selected'), word_wrap=True, min_width=200, max_width=300)
        self.select_output_dir_button = WidgetHelpers.configure_widget(widget=QPushButton('Select Output Directory'), min_width=170, max_width=180, click_handler=self.select_output_directory)
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.select_output_dir_button)
        self.file_section_layout.addLayout(
            output_dir_layout
        )

    def generate_action_btn_layout(self):
        action_btn_layout = QHBoxLayout()
        self.action_btn = WidgetHelpers.configure_widget(widget=QPushButton(self.action_btn_label), min_width=170, max_width=180, click_handler=self.action_btn_handler)
        action_btn_layout.addWidget(
            self.action_btn
        )
        self.progress_label = WidgetHelpers.configure_widget(widget=QLabel("Waiting to process files..."), set_visible=False, word_wrap=True)
        action_btn_layout.addWidget(
            self.progress_label
        )
        self.progress_bar = WidgetHelpers.configure_widget(widget=QProgressBar(self), set_minimum=0, set_value=0, set_visible=False)
        action_btn_layout.setAlignment(Qt.AlignCenter)
        self.file_section_layout.addLayout(action_btn_layout)

    def generate_additional_layouts(self):
        if self.additional_layouts is not None:
            for layout in self.additional_layouts:
                self.file_section_layout.addLayout(layout)

    def select_input_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if dir_path:
            self.input_dir = dir_path
            self.input_dir_label.setText(f"Input Directory: {dir_path}")
            print(f"Input Directory: {dir_path}")

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.setText(f"Output Directory: {dir_path}")
            print(f"Input Directory: {dir_path}")

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
