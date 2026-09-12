from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QApplication
from PyQt6.QtCore import QTimer, Qt
from ui.wizard import WizardWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accessible Gitignore Generator")
        self.setAccessibleName("Accessible Gitignore Generator")
        self.resize(700, 550)

        self.central = QWidget()
        self.central.setAccessibleName("Hlavní okno")
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)

        # Intro widget
        self.intro_widget = QWidget()
        self.intro_widget.setAccessibleName("Úvod")
        intro_layout = QVBoxLayout(self.intro_widget)

        title = QLabel("<h1>Průvodce vytvořením .gitignore</h1>")
        title.setWordWrap(True)
        title.setAccessibleName("Průvodce vytvořením .gitignore")
        intro_layout.addWidget(title)

        text = QLabel("Pomocí několika otázek vytvoříte soubor .gitignore přizpůsobený vašemu projektu.")
        text.setWordWrap(True)
        text.setAccessibleName("Pomocí několika otázek vytvoříte soubor .gitignore přizpůsobený vašemu projektu.")
        intro_layout.addWidget(text)

        # Buttons row
        btn_row = QWidget()
        row_layout = QHBoxLayout(btn_row)
        row_layout.setContentsMargins(0, 12, 0, 0)
        self.btn_start = QPushButton("Začít")
        self.btn_start.setAccessibleName("Začít")
        self.btn_start.setAccessibleDescription("Spustit průvodce vytvořením souboru .gitignore")
        self.btn_start.clicked.connect(self.on_start)
        row_layout.addWidget(self.btn_start)

        self.btn_exit = QPushButton("Ukončit")
        self.btn_exit.setAccessibleName("Ukončit")
        self.btn_exit.clicked.connect(self.close)
        row_layout.addWidget(self.btn_exit)

        self.btn_open_existing = QPushButton("Otevřít existující .gitignore")
        self.btn_open_existing.setAccessibleName("Otevřít existující .gitignore")
        self.btn_open_existing.clicked.connect(self.on_open_existing)
        row_layout.addWidget(self.btn_open_existing)
        row_layout.addStretch()

        intro_layout.addWidget(btn_row)
        intro_layout.addStretch()

        self.main_layout.addWidget(self.intro_widget)

        # Wizard widget (hidden initially)
        self.wizard = WizardWidget()
        self.wizard.finished_wizard.connect(self.on_wizard_finished)
        self.wizard.cancelled.connect(self.on_wizard_cancelled)
        self.wizard.hide()
        self.main_layout.addWidget(self.wizard)

        self._focused = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self._focused:
            self._focused = True
            QTimer.singleShot(0, self.btn_start.setFocus)

    def on_start(self):
        self.intro_widget.hide()
        self.wizard.show()
        # reset wizard to start
        self.wizard.current_index = 0
        # reset config
        from core.models import WizardConfig
        self.wizard.config = WizardConfig()
        for p in self.wizard.pages:
            p.load_from_config(self.wizard.config)
        self.wizard.stack.setCurrentIndex(0)
        self.wizard.update_nav()
        QTimer.singleShot(0, self.wizard.focus_current)

    def on_wizard_finished(self):
        self.wizard.hide()
        self.intro_widget.show()
        QTimer.singleShot(0, self.btn_start.setFocus)

    def on_wizard_cancelled(self):
        self.wizard.hide()
        self.intro_widget.show()
        QTimer.singleShot(0, self.btn_start.setFocus)

    def on_open_existing(self):
        path, _ = QFileDialog.getOpenFileName(self, "Otevřít .gitignore", "", "Git ignore files (*.gitignore);;All files (*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                # show wizard directly at preview with loaded content
                self.intro_widget.hide()
                self.wizard.show()
                # set config to generic to generate preview then override text
                from core.models import WizardConfig
                # Keep wizard config as is but load preview content
                self.wizard.current_index = len(self.wizard.pages) - 1
                self.wizard.stack.setCurrentIndex(self.wizard.current_index)
                self.wizard.update_nav()
                self.wizard.page_preview.text_edit.setPlainText(content)
                QTimer.singleShot(0, self.wizard.page_preview.text_edit.setFocus)
            except Exception as e:
                QMessageBox.warning(self, "Chyba", f"Nepodařilo se otevřít soubor: {e}")
