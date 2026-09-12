from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from core.validator import validate_custom_rule


class HelpDialog(QDialog):
    def __init__(self, parent, title: str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setAccessibleName(title)
        layout = QVBoxLayout(self)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAccessibleName(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        layout.addWidget(label)
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btn_box.setAccessibleName("Zavřít")
        close_btn = btn_box.button(QDialogButtonBox.StandardButton.Close)
        close_btn.setText("Zavřít")
        close_btn.setAccessibleName("Zavřít")
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self._close_btn = close_btn

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._close_btn.setFocus)


class CustomRuleDialog(QDialog):
    def __init__(self, parent, existing: list[str] | None = None):
        super().__init__(parent)
        self.setWindowTitle("Přidat vlastní pravidlo")
        self.setModal(True)
        self.setAccessibleName("Přidat vlastní pravidlo")
        self.existing = existing or []
        layout = QVBoxLayout(self)

        info = QLabel("Zadejte pravidlo pro .gitignore. Například: secrets/ nebo my_local_data/")
        info.setWordWrap(True)
        info.setAccessibleName("Zadejte pravidlo pro .gitignore. Například: secrets/ nebo my_local_data/")
        layout.addWidget(info)

        self.pattern_edit = QLineEdit()
        self.pattern_edit.setPlaceholderText("např. secrets/")
        self.pattern_edit.setAccessibleName("Pravidlo")
        self.pattern_edit.setAccessibleDescription("Zadejte cestu nebo vzor pro ignorování, například secrets/")
        layout.addWidget(QLabel("Pravidlo:"))
        layout.addWidget(self.pattern_edit)

        self.comment_edit = QLineEdit()
        self.comment_edit.setPlaceholderText("volitelný komentář")
        self.comment_edit.setAccessibleName("Komentář")
        self.comment_edit.setAccessibleDescription("Volitelný komentář k pravidlu")
        layout.addWidget(QLabel("Komentář (volitelné):"))
        layout.addWidget(self.comment_edit)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setText("Přidat")
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setAccessibleName("Přidat")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Zrušit")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setAccessibleName("Zrušit")
        btn_box.accepted.connect(self.on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self._pattern_edit = self.pattern_edit

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._pattern_edit.setFocus)

    def on_accept(self):
        pattern = self.pattern_edit.text()
        err = validate_custom_rule(pattern, self.existing)
        if err:
            QMessageBox.warning(self, "Chyba", err)
            return
        self.accept()

    def get_data(self):
        return self.pattern_edit.text().strip(), self.comment_edit.text().strip()


def show_info(parent, title: str, text: str):
    box = QMessageBox(parent)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(QMessageBox.Icon.Information)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    box.button(QMessageBox.StandardButton.Ok).setText("OK")
    box.button(QMessageBox.StandardButton.Ok).setAccessibleName("OK")
    box.setAccessibleName(title)
    box.exec()
