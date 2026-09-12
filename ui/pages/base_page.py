from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer


class BasePage(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.page_title = title
        self.setAccessibleName(title)
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(12, 12, 12, 12)
        self.layout_.setSpacing(8)
        title_label = QLabel(f"<h2>{title}</h2>")
        title_label.setAccessibleName(title)
        title_label.setWordWrap(True)
        self.layout_.addWidget(title_label)
        self._first_widget = None

    def set_first_widget(self, w: QWidget):
        self._first_widget = w

    def focus_first(self):
        if self._first_widget:
            QTimer.singleShot(0, self._first_widget.setFocus)

    def get_config_updates(self, config):
        """Override to update config from UI"""
        pass

    def load_from_config(self, config):
        """Override to set UI from config"""
        pass

    def validate_page(self):
        """Return error message or None"""
        return None
