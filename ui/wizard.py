from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QMessageBox, QFileDialog, QApplication, QLabel
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt
from core.models import WizardConfig, VenvAnswer, TestingAnswer, BuildAnswer, SecretAnswer
from ui.pages.project_type_page import ProjectTypePage
from ui.pages.venv_page import VenvAnswerPage, VenvNamePage
from ui.pages.ide_page import IdePage
from ui.pages.testing_page import TestingAnswerPage, TestingToolPage
from ui.pages.build_page import BuildAnswerPage, BuildToolPage
from ui.pages.data_page import DataPage
from ui.pages.secrets_page import SecretsAnswerPage, SecretsOptionsPage
from ui.pages.custom_rules_page import CustomRulesPage
from ui.pages.preview_page import PreviewPage, SaveWorker
from ui.accessibility import announce, show_accessible_warning, show_accessible_question
from core.generator import generate


class WizardWidget(QWidget):
    finished_wizard = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = WizardConfig()
        self.layout_ = QVBoxLayout(self)
        self.stack = QStackedWidget()
        self.stack.setAccessibleName("Průvodce")
        self.layout_.addWidget(self.stack)

        self.pages = []
        self._create_pages()

        # PKIE vzor: skrytá živá oblast pro oznamování změny stránky
        self.announcer = QLabel(self)
        self.announcer.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.announcer.setAccessibleName("Oznámení průvodce")
        self.announcer.hide()
        self.layout_.addWidget(self.announcer)

        # navigation
        nav = QWidget()
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(0, 8, 0, 0)
        self.btn_prev = QPushButton("Předchozí")
        self.btn_prev.setAccessibleName("Předchozí")
        self.btn_prev.setAccessibleDescription("Přejít na předchozí krok průvodce")
        self.btn_prev.clicked.connect(self.on_prev)

        self.btn_next = QPushButton("Další")
        self.btn_next.setAccessibleName("Další")
        self.btn_next.setAccessibleDescription("Přejít na další krok průvodce")
        self.btn_next.clicked.connect(self.on_next)

        self.btn_finish = QPushButton("Dokončit")
        self.btn_finish.setAccessibleName("Dokončit")
        self.btn_finish.setAccessibleDescription("Uložit výsledný .gitignore")
        self.btn_finish.clicked.connect(self.on_finish)

        self.btn_cancel = QPushButton("Zrušit")
        self.btn_cancel.setAccessibleName("Zrušit")
        self.btn_cancel.setAccessibleDescription("Zrušit průvodce, změny budou ztraceny")
        self.btn_cancel.clicked.connect(self.on_cancel)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addWidget(self.btn_finish)
        nav_layout.addWidget(self.btn_cancel)
        nav_layout.addStretch()
        self.layout_.addWidget(nav)

        self.current_index = 0
        self.stack.setCurrentIndex(0)
        self.update_nav()
        QTimer.singleShot(0, self.focus_current)

        self._save_worker = None

    def _create_pages(self):
        self.page_project = ProjectTypePage()
        self.page_venv_ans = VenvAnswerPage()
        self.page_venv_name = VenvNamePage()
        self.page_ide = IdePage()
        self.page_testing_ans = TestingAnswerPage()
        self.page_testing_tool = TestingToolPage()
        self.page_build_ans = BuildAnswerPage()
        self.page_build_tool = BuildToolPage()
        self.page_data = DataPage()
        self.page_secrets_ans = SecretsAnswerPage()
        self.page_secrets_opt = SecretsOptionsPage()
        self.page_custom = CustomRulesPage()
        self.page_preview = PreviewPage()

        for p in [self.page_project, self.page_venv_ans, self.page_venv_name, self.page_ide,
                  self.page_testing_ans, self.page_testing_tool, self.page_build_ans, self.page_build_tool,
                  self.page_data, self.page_secrets_ans, self.page_secrets_opt, self.page_custom, self.page_preview]:
            self.stack.addWidget(p)
            self.pages.append(p)

    def is_page_visible(self, idx: int) -> bool:
        page = self.pages[idx]
        if page == self.page_venv_name:
            return self.config.venv_answer == VenvAnswer.ANO
        if page == self.page_testing_tool:
            return self.config.testing_answer == TestingAnswer.ANO
        if page == self.page_build_tool:
            return self.config.build_answer == BuildAnswer.ANO
        if page == self.page_secrets_opt:
            return self.config.secret_answer == SecretAnswer.ANO
        return True

    def save_current_to_config(self):
        current = self.pages[self.current_index]
        current.get_config_updates(self.config)

    def load_current_from_config(self):
        current = self.pages[self.current_index]
        current.load_from_config(self.config)

    def focus_current(self):
        page = self.pages[self.current_index]
        page.focus_first()

    def _announce_page(self):
        """PKIE vzor: oznámení změny stránky – pouze jedno hlášení, bez duplicity."""
        page = self.pages[self.current_index]
        total = len([i for i in range(len(self.pages)) if self.is_page_visible(i) or i == self.current_index])
        # počítat viditelné kroky pro lepší kontext
        visible_count = sum(1 for i in range(len(self.pages)) if self.is_page_visible(i))
        # najít pořadí aktuální stránky mezi viditelnými
        order = sum(1 for i in range(self.current_index + 1) if self.is_page_visible(i) or i == self.current_index)
        title = getattr(page, "page_title", "")
        text = f"{title}, krok {order} z {visible_count}"
        announce(text, self)

    def update_nav(self):
        is_first = self.current_index == 0
        is_last = self.current_index == len(self.pages) - 1
        # skip hidden pages pro is_last logiku
        # najdi poslední viditelný
        last_visible = len(self.pages) - 1
        while last_visible >= 0 and not self.is_page_visible(last_visible):
            last_visible -= 1
        is_last = self.current_index == last_visible
        self.btn_prev.setEnabled(not is_first)
        self.btn_next.setEnabled(not is_last)
        self.btn_finish.setEnabled(is_last)

    def on_next(self):
        current = self.pages[self.current_index]
        err = current.validate_page()
        if err:
            show_accessible_warning(self, "Chyba", err)
            return
        current.get_config_updates(self.config)
        nxt = self.current_index + 1
        while nxt < len(self.pages) and not self.is_page_visible(nxt):
            nxt += 1
        if nxt >= len(self.pages):
            return
        self.current_index = nxt
        if self.pages[self.current_index] == self.page_preview:
            self.page_preview.generate_preview(self.config)
        self.stack.setCurrentIndex(self.current_index)
        self.update_nav()
        self._announce_page()
        self.focus_current()

    def on_prev(self):
        self.pages[self.current_index].get_config_updates(self.config)
        prev = self.current_index - 1
        while prev >= 0 and not self.is_page_visible(prev):
            prev -= 1
        if prev < 0:
            return
        self.current_index = prev
        self.stack.setCurrentIndex(self.current_index)
        self.update_nav()
        self._announce_page()
        self.focus_current()

    def on_finish(self):
        content = self.page_preview.get_content()
        if not content.strip():
            show_accessible_warning(self, "Chyba", "Obsah .gitignore je prázdný.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Uložit .gitignore", ".gitignore", "Git ignore files (*.gitignore);;All files (*)")
        if not path:
            return
        self._save_worker = SaveWorker(path, content)
        self._save_worker.finished_ok.connect(self.on_save_ok)
        self._save_worker.failed.connect(self.on_save_fail)
        self._save_worker.start()
        self.btn_finish.setEnabled(False)
        announce("Ukládám soubor, prosím čekejte", self)

    def on_save_ok(self, path):
        self.btn_finish.setEnabled(True)
        # PKIE vzor: nejdřív inline oznámení, pak dialog s 200ms odstupem aby se nebil s NVDA
        announce(f"Soubor .gitignore byl úspěšně uložen: {path}", self)
        # QTimer.singleShot jako PKIE FinishPage.on_build_finished
        def _show():
            box = QMessageBox(self)
            box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
            box.setWindowTitle("Uložení dokončeno")
            box.setText("Soubor .gitignore byl úspěšně uložen.")
            box.setInformativeText(path)
            box.setIcon(QMessageBox.Icon.Information)
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            btn = box.button(QMessageBox.StandardButton.Ok)
            if btn:
                btn.setText("OK")
                btn.setAccessibleName("OK")
            box.setAccessibleName(f"Uložení dokončeno. Soubor byl uložen: {path}")
            box.exec()
            self.finished_wizard.emit()
        QTimer.singleShot(200, _show)

    def on_save_fail(self, err):
        self.btn_finish.setEnabled(True)
        announce(f"Chyba při ukládání: {err}", self)
        QTimer.singleShot(200, lambda: show_accessible_warning(self, "Chyba", f"Nepodařilo se uložit soubor: {err}"))

    def on_cancel(self):
        if show_accessible_question(self, "Zrušit", "Opravdu chcete zrušit průvodce? Neuložené změny budou ztraceny."):
            self.cancelled.emit()
