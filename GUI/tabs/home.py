import os
import shutil
import subprocess
import sys
from typing import Optional, Callable

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog, QProgressBar, QGroupBox, QCheckBox, QSpinBox

from GUI.utils.core import WidgetHelpers
from GUI.widgets.file_section.controls import FileSectionControls
from GUI.widgets.file_section.ui import FileSectionParent
from GUI.widgets.file_section.workers import FileRenameAndMoveWorker
from controllers.name_generator import NameGenerator


def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.normpath(os.path.join(sys._MEIPASS, relative_path))
    return os.path.normpath(os.path.join(os.getcwd(), relative_path))

# Paths to ffmpeg and ffprobe
ffmpeg_path = resource_path('resources/ffmpeg/bin/ffmpeg.exe')
ffprobe_path = resource_path('resources/ffmpeg/bin/ffprobe.exe')

# Add ffmpeg's directory to PATH
ffmpeg_dir = os.path.dirname(ffmpeg_path)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Debugging: Check if ffmpeg is found in PATH
print("PATH Environment Variable:", os.environ["PATH"])

# Import PyDub and set paths
from pydub import AudioSegment
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path
from pydub.silence import detect_nonsilent

# Debugging information
print("FFmpeg Path:", AudioSegment.converter)
print("FFprobe Path:", AudioSegment.ffprobe)
# from controllers.name_generator import NameGenerator
# def get_logo_path():
#     """Resolve the path to ffmpeg.exe for both development and packaged modes."""
#     if getattr(sys, "frozen", False):  # Check if running in a packaged mode
#         base_path = sys._MEIPASS       # PyInstaller's temp directory
#     else:
#         base_path = os.path.dirname(__file__)  # Development mode
#
#     return os.path.join("GUI", "assets", "LemonCable.png")

# LEMON_CABLE_APP_LOGO_PATH = os.path.join(os.getcwd(), 'GUI', 'assets', "LemonCable.png")
LEMON_CABLE_APP_LOGO_PATH = resource_path('GUI/assets/LemonCable.png')
print("resource_path('resources/ffmpeg/ffmpeg.exe')")
print(resource_path('resources/ffmpeg/ffmpeg.exe'))
# AudioSegment.converter = os.path.join(os.getcwd(), 'resources', 'ffmpeg', "ffmpeg.exe")

print('LEMON_CABLE_APP_LOGO_PATH')
print(LEMON_CABLE_APP_LOGO_PATH)


class HomeUI(QWidget):

    SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trim_silence_worker = None
        self.name_album_settings_section = None
        self.songs_per_album_count_input = None
        self.album_music_name_worker = None
        self.songs_per_album_label = None
        self.make_multiple_albums_checkbox: Optional[QCheckBox] = None
        self.input_dir = None
        self.rename_output_dir = None
        self.rename_input_dir = None
        self.progress_bar = None
        self.output_dir = None
        self.random_name_button = None
        self.random_name_label = None
        self.random_name_section = None
        self.layout = None
        self.text_input = None
        self.selector_input = None
        self.url_input = None
        self.step_type = None
        self.form_layout = None
        self.step_list = None
        self.trim_silence_section: Optional[FileSectionParent] = None
        self.album_namer_section: Optional[FileSectionParent] = None
        self.steps = []  # Store all created steps
        self.namer = NameGenerator()

        self.init_ui()

    def init_ui(self):
        # TODO this could potentially be made into it's own class later
        self.layout = QVBoxLayout()

        self.create_logo()
        self.generate_random_name_section()
        self.build_input_output_trim_sound_dir_section()
        self.build_file_rename_move_section()
        # self.create_progress_bar()
        self.setLayout(self.layout)

    def generate_random_name_section(self):
        # Input directory layout
        self.random_name_section = QHBoxLayout()
        self.random_name_label = QLabel("Click the button to update this text")
        self.random_name_label.setAlignment(Qt.AlignCenter)
        self.random_name_label.setObjectName("RandomNameLabelEmpty")

        # Create the button
        self.random_name_button = QPushButton("Generate Name")
        self.random_name_button.setObjectName("RandomNameButton")
        self.random_name_button.clicked.connect(self.update_random_name_label)

        # Add label and button to the layout
        self.random_name_section.addWidget(self.random_name_label)
        self.random_name_section.addWidget(self.random_name_button)

        self.layout.addLayout(self.random_name_section)

    def create_logo(self) -> None:
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_label = QLabel(self)
        pixmap = QPixmap(LEMON_CABLE_APP_LOGO_PATH)

        if pixmap.isNull():
            print(f"Failed to load image: {LEMON_CABLE_APP_LOGO_PATH}")
            logo_label.setText("Logo failed to load.")
        else:
            scaled_pixmap = pixmap.scaled(500, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)

        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setObjectName("logo_label")
        logo_label.setMinimumSize(500, 250)
        logo_layout.addWidget(logo_label)

        self.layout.addLayout(logo_layout)

    def update_random_name_label(self):
        """Update the label text and apply a new style."""
        self.random_name_label.setText(self.namer.generate_title())
        self.random_name_label.setObjectName('RandomNameLabelWithName')

    def build_input_output_trim_sound_dir_section(self):
        # We should have this file section either accept a thread or except a method for a thread which will cause this object ot create a thread?
        self.trim_silence_section = FileSectionParent(
            section_label="Trim Silence From Audio Files",
            action_button_label="Trim Silence",
            action_btn_handler=self.clean_music,
            additional_layouts=None
        )
        self.layout.addWidget(self.trim_silence_section)

    def build_file_rename_move_section(self):
        self.name_album_settings_section = self.build_album_settings_section()
        self.album_namer_section = FileSectionParent(
            section_label="Generate Song Names for Albums and Files",
            action_button_label="Generate Song Names",
            action_btn_handler=self.rename_and_move_files,
            additional_layouts=[self.name_album_settings_section]
        )
        self.layout.addWidget(self.album_namer_section)

    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            print("Checkbox is checked!")
        elif state == Qt.Unchecked:
            print("Checkbox is unchecked!")

    def build_album_settings_section(self) -> QHBoxLayout:
        settings_layout = QHBoxLayout()
        checkbox_layout = QHBoxLayout()

        self.make_multiple_albums_checkbox = WidgetHelpers.configure_widget(widget=QCheckBox("For All Files In Input Directory?"), set_checked=False, state_change_handler=self.on_checkbox_state_changed)

        checkbox_layout.addWidget(self.make_multiple_albums_checkbox)
        settings_layout.addLayout(checkbox_layout)
        settings_layout.setAlignment(Qt.AlignCenter)

        spinbox_layout = QHBoxLayout()  # To position the label and spinbox horizontally
        self.songs_per_album_label = WidgetHelpers.configure_widget(
            QLabel("Number of Songs Per Album:"),
            object_name='AlbumSettingsLabel'
        )
        self.songs_per_album_count_input = WidgetHelpers.configure_widget(
            QSpinBox(),
            set_minimum=1,
            set_maximum=1000,
            set_value=30
        )

        spinbox_layout.addWidget(self.songs_per_album_label)
        spinbox_layout.addWidget(self.songs_per_album_count_input)
        settings_layout.addLayout(spinbox_layout)
        settings_layout.setObjectName('AlbumSettingsDiv')
        return settings_layout

    def rename_and_move_files(self):
        if not self.album_namer_section.input_dir or not self.album_namer_section.input_dir:
            QMessageBox.warning(self, "Missing Directories", "Please select both input and output directories.")
            return

        self.album_music_name_worker = FileRenameAndMoveWorker(self.album_namer_section.input_dir, self.album_namer_section.input_dir, ['.mp3', '.wav', '.ogg'], self.namer, is_multiple_albums=self.make_multiple_albums_checkbox.isChecked(), amount_per_album=self.songs_per_album_count_input.value())
        self.album_music_name_worker.progress.connect(lambda total_files, file_index: self.update_progress_bar(self.album_namer_section, total_files, file_index))
        self.album_music_name_worker.finished.connect(lambda success_count, error_count: self.on_complete('Trim Silence', success_count, error_count))
        self.album_music_name_worker.error.connect(lambda message: self.on_cleaning_error(self.album_namer_section, message))
        WidgetHelpers.configure_widget(self.album_namer_section.progress_bar, set_value=0, set_visible=True)
        # self.album_namer_section.pr.pr self.rename_progress_bar.setMaximum(len(os.listdir(self.rename_input_dir)))
        # self.rename_progress_bar.setValue(0)
        # self.rename_progress_bar.setVisible(True)
        self.album_namer_section.progress_label.setVisible(True)
        self.album_music_name_worker.start()

    def clean_music(self):
        if not self.trim_silence_section.input_dir or not self.trim_silence_section.output_dir:
            QMessageBox.warning(self, "Error", "Please select both input and output directories.")
            return

        # Initialize the worker thread
        self.trim_silence_worker = MusicCleanerWorker(self.input_dir, self.output_dir, self.SUPPORTED_EXTENSIONS)
        self.trim_silence_worker.progress.connect(lambda total_files, file_index: self.update_progress_bar(self.trim_silence_section, total_files, file_index))
        self.trim_silence_worker.finished.connect(lambda success_count, error_count: self.on_complete('Trim Silence', success_count, error_count))
        self.trim_silence_worker.error.connect(lambda message: self.on_cleaning_error(self.trim_silence_section, message))

        self.trim_silence_section.progress_bar.setMaximum(len(os.listdir(self.input_dir)))
        WidgetHelpers.configure_widget(self.trim_silence_section.progress_bar, set_value=0, set_visible=True)

        self.trim_silence_section.progress_label.setVisible(True)

        FileSectionControls.convert_action_btn_to_cancel_btn(self.trim_silence_section.action_btn, lambda _: self.on_cancel(self.trim_silence_section, self.trim_silence_worker))
        self.trim_silence_worker.start()

    def update_progress_bar(self, file_section: FileSectionParent, total_files, file_index):
        file_section.progress_bar.setValue(file_index)
        file_section.progress_label.setText(f"{file_index} out of {total_files} files")

    def on_complete(self, action_btn_text: str, success_count: int, error_count: int):
        FileSectionControls.update_progress_widgets_on_finish(self.trim_silence_section.progress_bar, self.trim_silence_section.progress_label, 'Completed!')
        FileSectionControls.convert_cancel_btn_to_action_btn(self.trim_silence_section.action_btn, self.clean_music, action_btn_text)
        QMessageBox.information(self, "Success", f"Music files processed successfully! \nSuccessful Files: {success_count}\nErrors: {error_count}")

    def on_cancel(self, file_section: FileSectionParent, worker: QThread):
        FileSectionControls.cancel_operation(self, file_section, worker)

    def on_cleaning_error(self, file_section: FileSectionParent, message: str):
        QMessageBox.warning(self, "Error", message)
        WidgetHelpers.configure_widget(file_section.progress_label, set_text=f"Error - {message}", set_visible=False)
