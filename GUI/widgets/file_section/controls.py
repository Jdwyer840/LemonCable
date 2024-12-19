from typing import Callable

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton

from GUI.widgets.file_section.ui import FileSectionParent


class FileSectionControls:

    @staticmethod
    def update_progress_widgets_on_finish(progress_bar: QWidget, progress_label: QWidget, message: str):
        progress_bar.setVisible(False)
        progress_label.setText(message)
        progress_label.setVisible(False)
        
    @staticmethod
    def stop_worker(worker: QThread):
        worker.stop()
        worker.quit()  # Safely terminate the thread
        worker.wait()
        
    @staticmethod
    def cancel_operation(widget: QWidget, file_section: FileSectionParent, worker: QThread):
        FileSectionControls.stop_worker(worker)
        FileSectionControls.update_progress_widgets_on_finish(file_section.progress_bar, file_section.progress_label, 'Cancelled!')
        QMessageBox.information(widget, "Cancelled!", f"Cancelled")
    
    @staticmethod
    def convert_action_btn_to_cancel_btn(btn: QPushButton, on_cancel_handler: Callable):
        btn.setText("Cancel")
        btn.setObjectName("CancelButton")
        btn.disconnect()
        btn.clicked.connect(on_cancel_handler)

    @staticmethod
    def convert_cancel_btn_to_action_btn(btn: QPushButton, action_handler: Callable, btn_text: str):
        btn.setText(btn_text)
        btn.setObjectName("")
        btn.disconnect()
        btn.clicked.connect(action_handler)
