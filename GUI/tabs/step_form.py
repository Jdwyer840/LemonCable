import json
from enum import Enum
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QFormLayout, QComboBox, QLineEdit, QPushButton, QMessageBox, QFileDialog

from webdriver.controller import WebDriverController


FROM_TEXT_STEP_MAP = {
    "Go To": {
        "type": "navigate",
        "url": ""
    },
    "Click": {
        "type": "click",
        "selector": ""
    },
    "Write": {
        "type": "write",
        "selector": "",
        "text": ""
    }
}


# class StepAction:
#
#     def __init__(self):


class FormHelpers(Enum):
    GO_TO = 'Go To'
    CLICK = 'Click'
    WRITE = 'Write'

    @classmethod
    def get_all_action_types_text(cls):
        return [action.value for action in cls]

    @staticmethod
    def get_driver_action_info_obj(action: str) -> dict | None:
        if action == FormHelpers.GO_TO:
            return {
                "type": "navigate",
                "url": ""
            }
        elif action == FormHelpers.CLICK:
            return {
                "type": "click",
                "selector": ""
            }
        elif action == FormHelpers.WRITE:
            return {
                "type": "write",
                "selector": "",
                "text": ""
            }
        else:
            print('Unrecognized Type!')
            return None


class StepForm(QWidget):
    """Dynamic form to create WebDriver steps."""
    def __init__(self, driver: WebDriverController = None, parent=None):
        self.driver = driver
        super().__init__(parent)
        self.text_input = None
        self.selector_input = None
        self.current_form = None
        self.url_input = None
        self.step_type = None
        self.form_layout = None
        self.step_list = None
        self.steps = []  # Store all created steps
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Step list display
        self.step_list = QListWidget()
        layout.addWidget(QLabel("Defined Steps:"))
        layout.addWidget(self.step_list)

        # Dynamic form
        self.form_layout = QFormLayout()
        self.step_type = QComboBox()
        print(" fuck " + str(FormHelpers.get_all_action_types_text()))
        self.step_type.addItems(FormHelpers.get_all_action_types_text())
        self.step_type.currentIndexChanged.connect(self.update_form_fields)

        self.url_input = QLineEdit()
        self.selector_input = QLineEdit()
        self.text_input = QLineEdit()

        # Initial form
        self.form_layout.addRow("Step Type:", self.step_type)
        self.form_layout.addRow("URL:", self.url_input)  # Shown only for "Go To"

        # Buttons
        self.add_step_button = QPushButton("Add Step")
        self.save_steps_button = QPushButton("Save Steps to JSON")

        self.add_step_button.clicked.connect(self.add_step)
        self.save_steps_button.clicked.connect(self.save_to_json)

        layout.addLayout(self.form_layout)
        layout.addWidget(self.add_step_button)
        layout.addWidget(self.save_steps_button)

        # Update form fields for the default selection
        self.update_form_fields()
        self.setLayout(layout)

    def update_form_fields(self):
        """Update form fields dynamically based on the selected step type."""
        # Remove all rows except the first (Step Type)
        while self.form_layout.rowCount() > 1:
            self.form_layout.removeRow(1)

        step_type = self.step_type.currentText()
        self.current_form = step_type
        if step_type == FormHelpers.GO_TO.value:
            url_input = QLineEdit()  # Create a new QLineEdit instance
            self.form_layout.addRow("URL:", url_input)
            self.url_input = url_input  # Save for later use
        elif step_type == FormHelpers.CLICK.value:
            selector_input = QLineEdit()  # Create a new QLineEdit instance
            self.form_layout.addRow("Selector:", selector_input)
            self.selector_input = selector_input  # Save for later use
        elif step_type == FormHelpers.WRITE.value:
            selector_input = QLineEdit()  # Create new QLineEdit instances
            text_input = QLineEdit()
            self.form_layout.addRow("Selector:", selector_input)
            self.form_layout.addRow("Text:", text_input)
            self.selector_input = selector_input  # Save for later use
            self.text_input = text_input  # Save for later use
        else:
            raise Exception("WTF IS THIS FORM TYPE")

    def add_step(self):
        """Add the current step to the list."""
        step_type = self.step_type.currentText()
        step = {"type": step_type}
        step_valid = True

        # Collect the appropriate data for the selected step type
        # if step_type == "navigate" and hasattr(self, 'url_input'):
        if step_type == FormHelpers.GO_TO.value and hasattr(self, 'url_input'):
            step["url"] = self.url_input.text()
            step["type"] = 'navigate'
        elif step_type == FormHelpers.CLICK.value and hasattr(self, 'selector_input'):
            step["selector"] = self.selector_input.text()
            step["type"] = 'click'
        elif step_type == FormHelpers.WRITE.value and hasattr(self, 'selector_input') and hasattr(self, 'text_input'):
            step["selector"] = self.selector_input.text()
            step["text"] = self.text_input.text()
            step["type"] = 'write'
        else:
            step_valid = False
            print('Unrecognized action')

        if step_valid:
            self.steps.append(step)
            self.step_list.addItem(f"{step_type}: {step}")
            self.clear_inputs()
            self.driver.add_task(step)

    def clear_inputs(self):
        """Clear the form inputs after adding a step."""
        # TODO bug here ensure that the correct input is showing before we do all this, hasAttr is the wrong way of doing this we need like a current

        if self.current_form == FormHelpers.GO_TO.value:
            self.url_input.clear()
        if self.current_form == FormHelpers.CLICK.value:
            self.selector_input.clear()
        if self.current_form == FormHelpers.WRITE.value:
            self.text_input.clear()
            self.selector_input.clear()

    def save_to_json(self):
        """Save steps to a JSON file."""
        if not self.steps:
            QMessageBox.warning(self, "No Steps", "Please add steps before saving.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Steps", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.steps, file, indent=4)
            QMessageBox.information(self, "Saved", f"Steps saved to {file_path}")
