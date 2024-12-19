import os
import shutil
import sys

from PyQt5.QtCore import pyqtSignal, QThread


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


class FileRenameAndMoveWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions, title_generator, is_multiple_albums, amount_per_album=30):
        super().__init__()
        self.errored_files = []
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.title_generator = title_generator  # Pass the title generator instance
        self.is_multiple_albums = is_multiple_albums
        self.amount_per_album = amount_per_album
        self.successes = 0

    def run(self):
        try:
            # Generate unique titles
            # TODO add database integration here to keep track of album titles
            # Get all files in the input directory
            files = [
                f for f in os.listdir(self.input_dir)
                if os.path.isfile(os.path.join(self.input_dir, f))
            ]
            files = files[0:self.amount_per_album] if not self.is_multiple_albums else files
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
                    if song_count == self.amount_per_album and not self.is_multiple_albums:
                        return

                    current_titles = list(self.title_generator.generate_unique_set_of_titles(used_titles=unique_album_names))
                    if not current_titles:
                        self.error.emit("Failed to generate unique titles.")
                        return

                    album_name: str = current_titles[0]
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
                    self.successes += 1

                except Exception as e:
                    print(f"Error processing file: {filename}: {e}")
                    self.errored_files.append(filename)
                    self.error.emit(f"Error processing file: {filename}: {e}")
                    continue

                # Update progress
                self.progress.emit(index + 1, total_files)

            self.finished.emit(self.successes, len(self.errored_files))
        except Exception as e:
            print(f"Error processing files: {str((e))}")
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


class MusicCleanerWorker(QThread):
    # TODO fmaybe pass these in?
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, supported_extensions):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.errored_files = []
        self.is_running = False
        self.successes = 0

    def run(self):
        try:
            self.is_running = True
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
                if not self.is_running:
                    break
                file_path = os.path.join(self.input_dir, filename)
                _, ext = os.path.splitext(filename)

                if ext.lower() not in self.supported_extensions:
                    continue

                try:
                    self.process_file(file_path, filename, index, total_files)
                    self.successes += 1
                except Exception as e:
                    self.errored_files.append(filename)
                    print(f"Error processing file: {filename}")
                    continue
            if self.errored_files:
                print(f"Errored processing some file(s) \nErrored Files: {' '.join(self.errored_files)}")
                self.error.emit(f"Errored processing some file(s) \nErrored Files: {' '.join(self.errored_files)}")

            # We could haave the cancel function have a signal or set something on the worker itself to
            self.finished.emit(self.successes, len(self.errored_files))
        except Exception as e:
            print(f"Error processing files: {str(e)}")
            self.error.emit(str(e))

    def process_file(self, file_path, filename, index, total_files):
        _, ext = os.path.splitext(filename)

        # Load the audio file
        audio = AudioSegment.from_file(file_path, format=ext.lstrip('.'))
        # TODO this is taking wayy too long , maybe try and optimize this shit more,
        # Detect nonsilent parts
        nonsilent_ranges = detect_nonsilent(
            audio, min_silence_len=2000, silence_thresh=-32
        )
        if not nonsilent_ranges:
            self.progress.emit(total_files, index)
            raise ValueError(f"No nonsilent audio detected in {filename}.")

        # Adjust start and end times to include 2-second buffers
        start_time = max(0, nonsilent_ranges[0][0] - 2000)
        end_time = min(len(audio), nonsilent_ranges[-1][1] + 2000)

        # Extract the trimmed audio
        trimmed_audio = audio[start_time:end_time]

        # Save to the output directory
        output_path = os.path.join(
            self.output_dir, f"{os.path.splitext(filename)[0]}_trimmed{ext}"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        trimmed_audio.export(output_path, format=ext.lstrip('.'))

        # Update progress
        self.progress.emit(total_files, index)

    def stop(self):
        self.is_running = False
