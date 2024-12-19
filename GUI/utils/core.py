from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QProgressBar, QCheckBox, QSpinBox


class WidgetHelpers:

    @staticmethod
    def configure_widget(widget: QWidget | QPushButton | QLabel | QSpinBox, **kwargs) -> QWidget | QPushButton | QLabel | QSpinBox:
        if 'word_wrap' in kwargs and isinstance(widget, QLabel):
            widget.setWordWrap(kwargs['word_wrap'])
        if 'min_width' in kwargs:
            widget.setMinimumWidth(kwargs['min_width'])
        if 'set_text' in kwargs:
            widget.setText(kwargs['set_text'])
        if 'max_width' in kwargs:
            widget.setMaximumWidth(kwargs['max_width'])
        if 'set_visible' in kwargs:
            widget.setVisible(kwargs['set_visible'])
        if 'set_minimum' in kwargs and hasattr(widget, 'setMinimum'):
            widget.setMinimum(kwargs['set_minimum'])
        if 'set_maximum' in kwargs and hasattr(widget, 'setMaximum'):
            widget.setMaximum(kwargs['set_maximum'])
        if 'set_value' in kwargs and hasattr(widget, 'setValue'):
            widget.setValue(kwargs['set_value'])
        if 'set_checked' in kwargs and isinstance(widget, QCheckBox):
            widget.setChecked(kwargs['set_checked'])
        if 'state_change_handler' in kwargs and isinstance(widget, QCheckBox):
            widget.stateChanged.connect(kwargs['state_change_handler'])  # noqa
        if 'click_handler' in kwargs and isinstance(widget, QPushButton):
            widget.clicked.connect(kwargs['click_handler'])  # noqa
        if 'object_name' in kwargs:
            widget.setObjectName(kwargs['object_name'])
        return widget
