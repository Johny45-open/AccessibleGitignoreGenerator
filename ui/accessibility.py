from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import QTimer


def set_accessible_name(widget: QWidget, name: str):
    widget.setAccessibleName(name)
    widget.setAccessibleDescription(name)


def create_label(text: str, buddy: QWidget | None = None, accessible_name: str | None = None) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextInteractionFlags(label.textInteractionFlags() | label.textInteractionFlags())
    if buddy is not None:
        label.setBuddy(buddy)
    if accessible_name:
        label.setAccessibleName(accessible_name)
    else:
        label.setAccessibleName(text)
    return label


def focus_widget_delayed(widget: QWidget):
    QTimer.singleShot(0, widget.setFocus)
