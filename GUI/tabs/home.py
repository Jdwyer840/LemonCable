import os
import shutil
import subprocess
import sys
from typing import Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog, QProgressBar, QGroupBox, QCheckBox, QSpinBox

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




class ScrollableMessageBox(QMessageBox):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Information)

        # Create a scrollable area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Add the message inside a QLabel
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        scroll_area.setWidget(message_label)

        # Add the scroll area to the QMessageBox layout
        scroll_widget = QWidget(self)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.addWidget(scroll_area)

        self.layout().addWidget(scroll_widget)


# TODO IDK what to call this yet, since the home tab is general, and whatever fuck you
class FileRenameAndMoveWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions, title_generator, is_multiple_albums, amount_per_album=30):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.title_generator = title_generator  # Pass the title generator instance
        self.is_multiple_albums = is_multiple_albums
        self.amount_per_album = amount_per_album

    def run(self):
        try:
            # Generate unique titles
            # TODO add database integration here to keep track of album titles
            # Get all files in the input directory
            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f))
            ]
            total_files = len(files)
            if total_files == 0:
                self.error.emit("No files found in the input directory.")
                return
            unique_album_names = self.get_album_names_from_albums_folder()
            current_titles = None
            album_name = 'album_name'
            song_count = 0
            album_folder_path = ''
            for index, filename in enumerate(files):
                if (not current_titles or len(current_titles) == 0) or song_count == self.amount_per_album:
                    current_titles = list(self.title_generator.generate_unique_set_of_titles(used_titles=unique_album_names))
                    if not current_titles:
                        self.error.emit("Failed to generate unique titles.")
                        return

                    album_name = current_titles[0]
                    song_count = 0
                    unique_album_names.add(album_name)

                    album_folder_path = os.path.join(self.output_dir, album_name)
                    os.makedirs(album_folder_path, exist_ok=True)

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
                    new_name = f"{current_titles.pop(0)}{ext}"

                    # Copy the file to the new folder with the new name
                    new_path = os.path.join(album_folder_path, new_name)
                    shutil.copy(file_path, new_path)
                    song_count = song_count + 1

                except Exception as e:
                    self.error.emit(f"Error processing {filename}: {e}")
                    continue

                # Update progress
                self.progress.emit(index + 1, total_files)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def get_album_names_from_albums_folder(self):
        # Output is where the albums go which are folders
        folder_names = set()
        try:
            if not os.path.exists(self.output_dir):
                print("Output directory does not exist.")
                return folder_names

            # Iterate through the directory
            for item in os.listdir(self.output_dir):
                item_path = os.path.join(self.output_dir, item)
                if os.path.isdir(item_path):  # Check if it's a folder
                    folder_names.add(item)

        except Exception as e:
            print(f"Error while reading directory: {e}")

        return folder_names


# TODO make this a standard class so we dont rewrite for the same shit
class MusicCleanerWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.errored_files = []
        self.successes = 0

    def run(self):
        try:
            if not os.path.isdir(self.input_dir):
                self.error.emit("Input directory does not exist.")
                return

            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f))
            ]
            total_files = len(files)
            if total_files == 0:
                self.error.emit("No files found in the input directory.")
                return

            for index, filename in enumerate(files):
                file_path = os.path.join(self.input_dir, filename)
                _, ext = os.path.splitext(filename)

                if ext.lower() not in self.supported_extensions:
                    continue

                try:
                    self.process_file(file_path, filename, index, total_files)
                    self.successes += 1
                except Exception as e:
                    self.errored_files.append(filename)
                    continue
            if self.errored_files:
                self.error.emit(f"Errored processing some file(s) \nErrored Files: {' '.join(self.errored_files)}")

            self.finished.emit(self.successes, len(self.errored_files))
        except Exception as e:
            self.error.emit(str(e))

    def process_file(self, file_path, filename, index, total_files):
        """Trim silence from the beginning and end of the audio file."""
        _, ext = os.path.splitext(filename)

        # Load the audio file
        audio = AudioSegment.from_file(file_path, format=ext.lstrip('.'))

        # Detect nonsilent parts
        nonsilent_ranges = detect_nonsilent(
            audio, min_silence_len=2000, silence_thresh=-40
        )
        if not nonsilent_ranges:
            raise ValueError(f"No nonsilent audio detected in {filename}.")

        # Extract the range from the first nonsilent frame to the last nonsilent frame
        start, end = nonsilent_ranges[0][0], nonsilent_ranges[-1][1]
        trimmed_audio = audio[start:end]

        # Save to the output directory
        output_path = os.path.join(
            self.output_dir, f"{os.path.splitext(filename)[0]}_trimmed{ext}"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        trimmed_audio.export(output_path, format=ext.lstrip('.'))

        # Update progress
        self.progress.emit(total_files, index)




class HomeUI(QWidget):

    SUPPORTED_EXTENSIONS = {'.mp3', '.wav', '.flac'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.songs_per_album_count_input = None
        self.album_music_name_worker = None
        self.songs_per_album_label = None
        self.make_multiple_albums_checkbox: Optional[QCheckBox] = None
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

        self.clean_progress_label = QLabel("Waiting to process files...")
        self.clean_progress_label.setVisible(False)  # Initially hidden
        self.clean_progress_label.setWordWrap(True)

        clean_music_layout.addWidget(self.clean_progress_label)
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

        self.rename_progress_label = QLabel("Waiting to process files...")
        self.rename_progress_label.setVisible(False)  # Initially hidden
        self.rename_progress_label.setWordWrap(True)

        rename_move_layout.addWidget(self.rename_progress_label)


        temp_shit = QHBoxLayout()
        checkbox_layout = QHBoxLayout()
        self.make_multiple_albums_checkbox = QCheckBox("Make Multiple Albums?")
        self.make_multiple_albums_checkbox.setChecked(False)  # Unchecked by default
        self.make_multiple_albums_checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        checkbox_layout.addWidget(self.make_multiple_albums_checkbox)
        temp_shit.addLayout(checkbox_layout)
        temp_shit.setAlignment(Qt.AlignCenter)

        spinbox_layout = QHBoxLayout()  # To position the label and spinbox horizontally
        self.songs_per_album_label = QLabel("Number of Songs Per Album:")
        self.songs_per_album_label.setObjectName('AlbumSettingsLabel')
        self.songs_per_album_count_input = QSpinBox()
        self.songs_per_album_count_input.setMinimum(1)  # Minimum value
        self.songs_per_album_count_input.setMaximum(1000)  # Maximum value
        self.songs_per_album_count_input.setValue(30)  # Default value

        spinbox_layout.addWidget(self.songs_per_album_label)
        spinbox_layout.addWidget(self.songs_per_album_count_input)
        temp_shit.addLayout(spinbox_layout)
        temp_shit.setObjectName('AlbumSettingsDiv')

        file_rename_move_layout.addLayout(temp_shit)
        # file_rename_move_layout.addLayout(checkbox_layout)
        # file_rename_move_layout.addLayout(spinbox_layout)
        self.rename_progress_bar = QProgressBar(self)
        self.rename_progress_bar.setMinimum(0)
        self.rename_progress_bar.setValue(0)
        self.rename_progress_bar.setVisible(False)  # Initially hidden
        rename_move_layout.addWidget(self.rename_progress_bar)

        file_rename_move_layout.addLayout(rename_move_layout)

        file_rename_move_group.setLayout(file_rename_move_layout)
        self.layout.addWidget(file_rename_move_group)

    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            print("Checkbox is checked!")
        elif state == Qt.Unchecked:
            print("Checkbox is unchecked!")

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

        self.album_music_name_worker = FileRenameAndMoveWorker(self.rename_input_dir, self.rename_output_dir, ['.mp3', '.wav', '.ogg'], self.namer, is_multiple_albums=self.make_multiple_albums_checkbox.isChecked(), amount_per_album=self.songs_per_album_count_input.value())
        self.album_music_name_worker.progress.connect(self.update_rename_progress)
        self.album_music_name_worker.finished.connect(self.on_rename_move_finished)
        self.album_music_name_worker.error.connect(self.show_error)
        self.rename_progress_bar.setMaximum(len(os.listdir(self.rename_input_dir)))
        self.rename_progress_bar.setValue(0)
        self.rename_progress_bar.setVisible(True)
        self.rename_progress_label.setVisible(True)

        self.album_music_name_worker.start()

    def update_rename_progress(self, file_index, total_files):
        """Update progress bar."""
        self.rename_progress_label.setText(f"{file_index} out of {total_files} files")
        self.rename_progress_bar.setValue(file_index)

    def on_rename_move_finished(self):
        """Handle successful file processing."""
        self.rename_progress_bar.setVisible(False)
        self.rename_progress_label.setText('Waiting...')
        self.rename_progress_label.setVisible(False)

        QMessageBox.information(self, "Success", "Files renamed and moved successfully!")

    def show_error(self, message):
        """Handle errors during file processing."""
        self.clean_progress_label.setText(f"Processing Status: Error - {message}")
        QMessageBox.critical(self, "Error", message)
        self.clean_progress_label.setVisible(False)


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
        self.clean_music_worker = MusicCleanerWorker(self.input_dir, self.output_dir, self.SUPPORTED_EXTENSIONS)
        self.clean_music_worker.progress.connect(self.update_progress_bar)
        self.clean_music_worker.finished.connect(self.on_cleaning_finished)
        self.clean_music_worker.error.connect(self.on_cleaning_error)

        # Prepare the progress bar
        self.progress_bar.setMaximum(len(os.listdir(self.input_dir)))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.clean_progress_label.setVisible(True)

        # Start the worker thread
        self.clean_music_worker.start()

    def update_progress_bar(self, total_files, file_index):
        self.progress_bar.setValue((file_index + 1) * 100 // total_files)
        self.clean_progress_label.setText(f"{file_index} out of {total_files} files")

    def on_cleaning_finished(self, success_count, error_count):
        self.progress_bar.setVisible(False)
        self.rename_progress_label.setText("Completed!")
        self.clean_progress_label.setVisible(False)
        QMessageBox.information(self, "Success", f"Music files processed successfully! \nSuccessful Files: {success_count}\nErrors: {error_count}")

    def on_cleaning_error(self, message):
        QMessageBox.warning(self, "Error", message)
        self.clean_progress_label.setText(f"Processing Status: Error - {message}")
        self.clean_progress_label.setVisible(False)


