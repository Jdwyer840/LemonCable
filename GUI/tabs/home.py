import os
import shutil
import subprocess
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog, QProgressBar, QGroupBox

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
# ffmpeg_path = os.path.join(sys.prefix, "Scripts", "ffmpeg.exe")
# AudioSegment.converter = ffmpeg_path


# def get_ffmpeg_path():
#     """Resolve the path to ffmpeg.exe for both development and packaged modes."""
#     if getattr(sys, "frozen", False):  # Packaged mode
#         base_path = sys._MEIPASS       # PyInstaller's temporary folder
#     else:
#         base_path = os.path.dirname(__file__)  # Development mode
#
#     return os.path.join(base_path, "resources", "ffmpeg", "ffmpeg.exe")
#
# def get_ffprobe_path():
#     """Resolve the path to ffprobe.exe for both development and packaged modes."""
#     if getattr(sys, "frozen", False):  # Packaged mode
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.dirname(__file__)
#
#     return os.path.join(base_path, "resources", "ffmpeg", "ffprobe.exe")
#
# # Set the FFmpeg paths for pydub
# AudioSegment.converter = get_ffmpeg_path()
# AudioSegment.ffprobe = get_ffprobe_path()


# TODO IDK what to call this yet, since the home tab is general, and whatever fuck you
class FileRenameAndMoveWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions, title_generator):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.title_generator = title_generator  # Pass the title generator instance

    def run(self):
        try:
            # Generate unique titles
            unique_titles = list(self.title_generator.generate_unique_set_of_titles())
            if not unique_titles:
                self.error.emit("Failed to generate unique titles.")
                return

            # Create the new folder in the output directory
            folder_name = unique_titles[0]  # First title becomes the folder name
            folder_path = os.path.join(self.output_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Get all files in the input directory
            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f))
            ]
            total_files = len(files)
            if total_files == 0:
                self.error.emit("No files found in the input directory.")
                return

            for index, filename in enumerate(files):
                file_path = os.path.normpath(os.path.normpath(os.path.join(self.input_dir, filename)))
                if not os.path.isfile(file_path):
                    continue

                _, ext = os.path.splitext(filename)
                if ext.lower() not in self.supported_extensions:
                    continue

                try:
                    # Generate a new name from the remaining unique titles
                    # if not unique_titles:
                    #     unique_titles = list(self.title_generator.generate_unique_set_of_titles())
                    new_name = f"{unique_titles.pop(0)}{ext}"

                    # Copy the file to the new folder with the new name
                    new_path = os.path.join(folder_path, new_name)
                    shutil.copy(file_path, new_path)

                except Exception as e:
                    self.error.emit(f"Error processing {filename}: {e}")
                    continue

                # Update progress
                self.progress.emit(index + 1)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


# TODO make this a standard class so we dont rewrite for the same shit
class MusicCleanerWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions

    def run(self):
        try:
            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f))
            ]
            total_files = len(files)
            if total_files == 0:
                self.error.emit("No files found in the input directory.")
                return

            for index, filename in enumerate(files):
                file_path = os.path.normpath(os.path.join(self.input_dir, filename))
                if not os.path.isfile(file_path):
                    continue

                _, ext = os.path.splitext(filename)
                if ext.lower() not in self.supported_extensions:
                    continue

                try:
                    audio = AudioSegment.from_file(file_path, format=ext.lstrip('.'))
                    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=2000, silence_thresh=-40)

                    # Combine nonsilent parts
                    trimmed_audio = AudioSegment.empty()
                    for start, end in nonsilent_ranges:
                        trimmed_audio += audio[start:end]

                    # Save to output directory with modified filename
                    original_name, ext = os.path.splitext(filename)
                    new_name = f"{original_name}_processed_{index}{ext}"
                    output_path = os.path.join(self.output_dir, new_name)
                    trimmed_audio.export(output_path, format=ext.lstrip('.'))
                except Exception as e:
                    self.error.emit(f"Error processing {filename}: {e}")
                    continue

                # Update progress
                self.progress.emit(index + 1)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))




class HomeUI(QWidget):

    SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_dir = None
        self.rename_output_dir = None
        self.rename_input_dir = None
        self.progress_bar = None
        self.output_dir = None
        self.rename_input_dir = None
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
        print("Button clicked yo")
        """Update the label text and apply a new style."""
        self.random_name_label.setText(self.namer.generate_title())
        self.random_name_label.setObjectName('RandomNameLabelWithName')

    def build_input_output_trim_sound_dir_section(self):
        strip_dead_sound_group = QGroupBox("Strip Dead Sound From Files")
        strip_dead_sound_layout = QVBoxLayout()


        input_dir_layout = QHBoxLayout()
        self.input_dir_label = QLabel("Input Directory: Not Selected")
        self.input_dir_label.setWordWrap(True)  # Allow text wrapping to a new line
        self.input_dir_label.setMinimumWidth(200)
        self.input_dir_label.setMaximumWidth(300)
        self.select_input_button = QPushButton("Select Input Directory")
        self.select_input_button.setMinimumWidth(170)
        self.select_input_button.setMaximumWidth(180)
        self.select_input_button.clicked.connect(self.select_input_directory)

        input_dir_layout.addWidget(self.input_dir_label)
        input_dir_layout.addWidget(self.select_input_button)
        strip_dead_sound_layout.addLayout(input_dir_layout)

        output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel("Output Directory: Not Selected")
        self.output_dir_label.setWordWrap(True)  # Allow text wrapping to a new line
        self.output_dir_label.setMinimumWidth(200)
        self.output_dir_label.setMaximumWidth(300)
        self.select_output_button = QPushButton("Select Output Directory")
        self.select_output_button.setMinimumWidth(170)
        self.select_output_button.setMaximumWidth(180)
        self.select_output_button.clicked.connect(self.select_output_directory)
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.select_output_button)

        strip_dead_sound_layout.addLayout(output_dir_layout)
        clean_music_layout = QHBoxLayout()
        self.clean_music_start_button = QPushButton("Clean Music")
        self.clean_music_start_button.setMinimumWidth(170)
        self.clean_music_start_button.setMaximumWidth(180)
        self.clean_music_start_button.clicked.connect(self.clean_music)
        clean_music_layout.addWidget(self.clean_music_start_button)
        clean_music_layout.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Initially hidden
        clean_music_layout.addWidget(self.progress_bar)
        strip_dead_sound_layout.addLayout(clean_music_layout)
        strip_dead_sound_group.setLayout(strip_dead_sound_layout)

        self.layout.addWidget(strip_dead_sound_group)

    def build_file_rename_move_section(self):
        file_rename_move_group = QGroupBox("Rename and Move Files")
        file_rename_move_layout = QVBoxLayout()

        input_dir_layout = QHBoxLayout()
        self.rename_input_dir_label = QLabel("Input Directory: Not Selected")
        self.rename_input_dir_label.setWordWrap(True)
        self.rename_input_dir_label.setMinimumWidth(200)
        self.rename_input_dir_label.setMaximumWidth(300)
        self.rename_select_input_button = QPushButton("Select Input Directory")
        self.rename_select_input_button.setMinimumWidth(170)
        self.rename_select_input_button.setMaximumWidth(180)
        self.rename_select_input_button.clicked.connect(self.select_rename_input_directory)

        input_dir_layout.addWidget(self.rename_input_dir_label)
        input_dir_layout.addWidget(self.rename_select_input_button)
        file_rename_move_layout.addLayout(input_dir_layout)

        output_dir_layout = QHBoxLayout()
        self.rename_output_dir_label = QLabel("Output Directory: Not Selected")
        self.rename_output_dir_label.setWordWrap(True)
        self.rename_output_dir_label.setMinimumWidth(200)
        self.rename_output_dir_label.setMaximumWidth(300)
        self.rename_select_output_button = QPushButton("Select Output Directory")
        self.rename_select_output_button.setMinimumWidth(170)
        self.rename_select_output_button.setMaximumWidth(180)
        self.rename_select_output_button.clicked.connect(self.select_rename_output_directory)

        output_dir_layout.addWidget(self.rename_output_dir_label)
        output_dir_layout.addWidget(self.rename_select_output_button)
        file_rename_move_layout.addLayout(output_dir_layout)

        rename_move_layout = QHBoxLayout()
        self.rename_move_start_button = QPushButton("Rename and Move Files")
        self.rename_move_start_button.setMinimumWidth(170)
        self.rename_move_start_button.setMaximumWidth(180)
        self.rename_move_start_button.clicked.connect(self.rename_and_move_files)
        rename_move_layout.addWidget(self.rename_move_start_button)
        rename_move_layout.setAlignment(Qt.AlignCenter)

        self.rename_progress_bar = QProgressBar(self)
        self.rename_progress_bar.setMinimum(0)
        self.rename_progress_bar.setValue(0)
        self.rename_progress_bar.setVisible(False)  # Initially hidden
        rename_move_layout.addWidget(self.rename_progress_bar)

        file_rename_move_layout.addLayout(rename_move_layout)

        file_rename_move_group.setLayout(file_rename_move_layout)
        self.layout.addWidget(file_rename_move_group)

    def select_rename_input_directory(self):
        # TODO reuse functions and pass in the details
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if selected_dir:
            self.rename_input_dir_label.setText(f"Input Directory: {selected_dir}")
            self.rename_input_dir = selected_dir

    def select_rename_output_directory(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if selected_dir:
            self.rename_output_dir_label.setText(f"Output Directory: {selected_dir}")
            self.rename_output_dir = selected_dir

    def rename_and_move_files(self):
        if not self.rename_input_dir or not self.rename_output_dir:
            QMessageBox.warning(self, "Missing Directories", "Please select both input and output directories.")
            return

        worker = FileRenameAndMoveWorker(self.rename_input_dir, self.rename_output_dir, ['.mp3', '.wav'], self.namer)
        worker.progress.connect(self.update_rename_progress)
        worker.finished.connect(self.on_rename_move_finished)
        worker.error.connect(self.show_error)
        self.rename_progress_bar.setMaximum(len(os.listdir(self.rename_input_dir)))
        self.rename_progress_bar.setValue(0)
        self.rename_progress_bar.setVisible(True)

        worker.start()

    def create_progress_bar(self):
        """Create and add the progress bar to the layout."""
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Initially hidden
        self.layout.addWidget(self.progress_bar)

        # TODO move this shit to the controller class

    def select_input_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if dir_path:
            self.input_dir = dir_path
            self.input_dir_label.setText(f"Input Directory: {dir_path}")

    def select_input_directory_SHARED(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if dir_path:
            self.input_dir = dir_path
            self.input_dir_label.setText(f"Input Directory: {dir_path}")

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.setText(f"Output Directory: {dir_path}")

    def clean_music(self):
        if not self.input_dir or not self.output_dir:
            QMessageBox.warning(self, "Error", "Please select both input and output directories.")
            return

        # Initialize the worker thread
        self.worker = MusicCleanerWorker(self.input_dir, self.output_dir, self.SUPPORTED_EXTENSIONS)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.finished.connect(self.on_cleaning_finished)
        self.worker.error.connect(self.on_cleaning_error)

        # Prepare the progress bar
        self.progress_bar.setMaximum(len(os.listdir(self.input_dir)))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Start the worker thread
        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def on_cleaning_finished(self):
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Success", "Music files processed successfully!")

    def on_cleaning_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def update_rename_progress(self, value):
        """Update progress bar."""
        self.rename_progress_bar.setValue(value)

    def on_rename_move_finished(self):
        """Handle successful file processing."""
        self.rename_progress_bar.setVisible(False)
        QMessageBox.information(self, "Success", "Files renamed and moved successfully!")

    def show_error(self, message):
        """Handle errors during file processing."""
        QMessageBox.critical(self, "Error", message)
