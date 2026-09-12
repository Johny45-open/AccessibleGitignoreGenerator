from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QApplication
)
from PyQt6.QtCore import QTimer, Qt
from core.validator import validate_custom_rule
from ui.accessibility import announce, show_accessible_warning


class HelpDialog(QDialog):
    def __init__(self, parent, title: str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAccessibleName(title)
        self.setAccessibleDescription(text)
        self._prev_widget = QApplication.focusWidget()
        layout = QVBoxLayout(self)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        label.setAccessibleName(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        layout.addWidget(label)
        self._info_label = label
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btn_box.setAccessibleName("Zavřít")
        close_btn = btn_box.button(QDialogButtonBox.StandardButton.Close)
        close_btn.setText("Zavřít")
        close_btn.setAccessibleName("Zavřít")
        close_btn.setAccessibleDescription(f"Zavřít dialog {title}")
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self._close_btn = close_btn

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._close_btn.setFocus)

    def done(self, r):
        super().done(r)
        # PKIE: obnova fokusu po zavrení dialogu
        if self._prev_widget is not None:
            try:
                QTimer.singleShot(0, self._prev_widget.setFocus)
            except RuntimeError:
                pass


class CustomRuleDialog(QDialog):
    def __init__(self, parent, existing: list[str] | None = None):
        super().__init__(parent)
        self.setWindowTitle("Přidat vlastní pravidlo")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAccessibleName("Přidat vlastní pravidlo")
        self.setAccessibleDescription("Dialog pro přidání vlastního pravidla do .gitignore")
        self._prev_widget = QApplication.focusWidget()
        self.existing = existing or []
        layout = QVBoxLayout(self)

        info = QLabel("Zadejte pravidlo pro .gitignore. Například: secrets/ nebo my_local_data/")
        info.setWordWrap(True)
        info.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        info.setAccessibleName("Zadejte pravidlo pro .gitignore. Například: secrets/ nebo my_local_data/")
        layout.addWidget(info)

        self.pattern_edit = QLineEdit()
        self.pattern_edit.setPlaceholderText("např. secrets/")
        self.pattern_edit.setAccessibleName("Pravidlo")
        self.pattern_edit.setAccessibleDescription("Zadejte cestu nebo vzor pro ignorování, například secrets/")
        lbl_pat = QLabel("Pravidlo:")
        lbl_pat.setBuddy(self.pattern_edit)
        layout.addWidget(lbl_pat)
        layout.addWidget(self.pattern_edit)

        self.comment_edit = QLineEdit()
        self.comment_edit.setPlaceholderText("volitelný komentář")
        self.comment_edit.setAccessibleName("Komentář")
        self.comment_edit.setAccessibleDescription("Volitelný komentář k pravidlu")
        lbl_com = QLabel("Komentář (volitelné):")
        lbl_com.setBuddy(self.comment_edit)
        layout.addWidget(lbl_com)
        layout.addWidget(self.comment_edit)

        # PKIE hint pro ctecku
        hint = QLabel("Použijte Tab pro přesun mezi poli, Enter pro přidání, Escape pro zrušení.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: palette(mid); font-size: 9pt;")
        layout.addWidget(hint)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setText("Přidat")
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setAccessibleName("Přidat")
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setAccessibleDescription("Přidat pravidlo do seznamu")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Zrušit")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setAccessibleName("Zrušit")
        btn_box.accepted.connect(self.on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self._pattern_edit = self.pattern_edit

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._pattern_edit.setFocus)

    def done(self, r):
        super().done(r)
        if self._prev_widget is not None:
            try:
                QTimer.singleShot(0, self._prev_widget.setFocus)
            except RuntimeError:
                pass

    def on_accept(self):
        pattern = self.pattern_edit.text()
        err = validate_custom_rule(pattern, self.existing)
        if err:
            show_accessible_warning(self, "Chyba", err)
            QTimer.singleShot(0, self.pattern_edit.setFocus)
            return
        self.accept()

    def get_data(self):
        return self.pattern_edit.text().strip(), self.comment_edit.text().strip()


def show_info(parent, title: str, text: str):
    box = QMessageBox(parent)
    box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(QMessageBox.Icon.Information)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    btn = box.button(QMessageBox.StandardButton.Ok)
    if btn:
        btn.setText("OK")
        btn.setAccessibleName("OK")
    box.setAccessibleName(f"{title}. {text}")
    box.setAccessibleDescription(text)
    box.exec()
