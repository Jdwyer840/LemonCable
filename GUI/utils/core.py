from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QProgressBar


class WidgetHelpers:

    @staticmethod
    def configure_widget(widget: QWidget | QPushButton, **kwargs) -> QWidget | QPushButton:
        if 'word_wrap' in kwargs:
            widget.setWordWrap(kwargs['word_wrap'])
        if 'min_width' in kwargs:
            widget.setMinimumWidth(kwargs['min_width'])
        if 'max_width' in kwargs:
            widget.setMaximumWidth(kwargs['max_width'])
        if 'set_visible' in kwargs:
            widget.setVisible(kwargs['set_visible'])
        if 'set_minimum' in kwargs and isinstance(widget, QProgressBar):
            widget.setMinimum(kwargs['set_minimum'])
        if 'set_value' in kwargs:
            widget.setValue(kwargs['set_value'])
        if 'click_handler' in kwargs and isinstance(widget, QPushButton):
            widget.clicked.connect(kwargs['click_handler'])  # noqa
        return widget

