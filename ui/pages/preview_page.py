from PyQt6.QtWidgets import QLabel, QTextEdit, QPushButton, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from ui.pages.base_page import BasePage
from ui.accessibility import announce, show_accessible_warning
from core.generator import generate
import os


class SaveWorker(QThread):
    finished_ok = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, path: str, content: str):
        super().__init__()
        self.path = path
        self.content = content

    def run(self):
        try:
            with open(self.path, "w", encoding="utf-8", newline="\n") as f:
                f.write(self.content)
            self.finished_ok.emit(self.path)
        except Exception as e:
            self.failed.emit(str(e))


class PreviewPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Náhled .gitignore", parent)
        info = QLabel("Níže je výsledný obsah souboru .gitignore. Můžete ho před uložením upravit.")
        info.setWordWrap(True)
        info.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        info.setAccessibleName("Níže je výsledný obsah souboru .gitignore. Můžete ho před uložením upravit.")
        self.layout_.addWidget(info)

        self.text_edit = QTextEdit()
        self.text_edit.setAccessibleName("Náhled .gitignore")
        self.text_edit.setAccessibleDescription("Výsledný obsah souboru .gitignore, lze upravovat")
        self.layout_.addWidget(self.text_edit)

        # PKIE vzor: inline stav pro živé oznámení
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.status_label.setAccessibleName("Stav náhledu")
        self.status_label.hide()
        self.layout_.addWidget(self.status_label)

        btn_row = QWidget()
        row = QHBoxLayout(btn_row)
        row.setContentsMargins(0, 0, 0, 0)
        self.btn_copy = QPushButton("Kopírovat do schránky")
        self.btn_copy.setAccessibleName("Kopírovat do schránky")
        self.btn_copy.setAccessibleDescription("Zkopírovat obsah náhledu do schránky")
        self.btn_copy.clicked.connect(self.on_copy)
        row.addWidget(self.btn_copy)

        self.btn_open = QPushButton("Otevřít existující .gitignore")
        self.btn_open.setAccessibleName("Otevřít existující .gitignore")
        self.btn_open.setAccessibleDescription("Načíst existující soubor do náhledu")
        self.btn_open.clicked.connect(self.on_open)
        row.addWidget(self.btn_open)
        row.addStretch()
        self.layout_.addWidget(btn_row)

        self.layout_.addStretch()
        self.set_first_widget(self.text_edit)
        self._save_worker = None

    def generate_preview(self, config):
        text = generate(config)
        self.text_edit.setPlainText(text)
        lines = len(text.strip().splitlines()) if text.strip() else 0
        msg = f"Náhled aktualizován, {lines} řádků. Můžete ho upravit před uložením."
        self.status_label.setText(msg)
        self.status_label.setAccessibleName(msg)
        self.status_label.show()
        announce(msg, self)

    def get_content(self) -> str:
        return self.text_edit.toPlainText()

    def on_copy(self):
        text = self.text_edit.toPlainText()
        if not text.strip():
            show_accessible_warning(self, "Informace", "Náhled je prázdný, není co kopírovat.")
            return
        QApplication.clipboard().setText(text)
        msg = "Obsah .gitignore byl zkopírován do schránky."
        self.status_label.setText(msg)
        self.status_label.setAccessibleName(msg)
        self.status_label.show()
        announce(msg, self)
        # PKIE: odstup 200ms aby se nebil status s dialogem
        def _show():
            box = QMessageBox(self)
            box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
            box.setWindowTitle("Zkopírováno")
            box.setText(msg)
            box.setIcon(QMessageBox.Icon.Information)
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            btn = box.button(QMessageBox.StandardButton.Ok)
            if btn:
                btn.setText("OK")
                btn.setAccessibleName("OK")
            box.setAccessibleName(msg)
            box.exec()
        QTimer.singleShot(200, _show)

    def on_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Otevřít .gitignore", "", "Git ignore files (*.gitignore);;All files (*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                msg = f"Soubor načten: {path}"
                self.status_label.setText(msg)
                self.status_label.setAccessibleName(msg)
                self.status_label.show()
                announce(msg, self)
                def _show():
                    box = QMessageBox(self)
                    box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
                    box.setWindowTitle("Otevřeno")
                    box.setText(msg)
                    box.setIcon(QMessageBox.Icon.Information)
                    box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    btn = box.button(QMessageBox.StandardButton.Ok)
                    if btn:
                        btn.setText("OK")
                        btn.setAccessibleName("OK")
                    box.setAccessibleName(msg)
                    box.exec()
                QTimer.singleShot(200, _show)
            except Exception as e:
                show_accessible_warning(self, "Chyba", f"Nepodařilo se otevřít soubor: {e}")
