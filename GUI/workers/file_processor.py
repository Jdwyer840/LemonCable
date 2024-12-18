from PyQt5.QtCore import QThread, pyqtSignal


class FileProcessorWorker(QThread):

    def __init__(self, progress_signal: pyqtSignal, finish_signal: pyqtSignal,
                 error_signal: pyqtSignal, input_dir: str, output_dir: str, supported_extensions: list[str]):
        super().__init__()
        self.progress_signal = progress_signal
        self.finish_signal = finish_signal
        self.error_signal = error_signal
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_extensions = supported_extensions
        self.errored_files = []
        self.is_running = False
        self.successes = 0
