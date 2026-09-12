from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QRadioButton, QLabel, QPushButton, QButtonGroup
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import BuildAnswer, BuildTool


class BuildAnswerPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 5 – Vytváření programu pro Windows", parent)
        q = QLabel("Vytváříte ze svého Python programu samostatný program pro Windows?")
        q.setWordWrap(True)
        q.setAccessibleName("Vytváříte ze svého Python programu samostatný program pro Windows?")
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_.addWidget(q)
        desc = QLabel("Například soubor EXE, který lze spustit i bez ručního spouštění Pythonu.")
        desc.setWordWrap(True)
        self.layout_.addWidget(desc)

        self.radio_ano = QRadioButton("Ano")
        self.radio_ano.setAccessibleName("Ano – vytvářím samostatný program")
        self.layout_.addWidget(self.radio_ano)

        self.radio_ne = QRadioButton("Ne")
        self.radio_ne.setAccessibleName("Ne – nevytvářím samostatný program")
        self.layout_.addWidget(self.radio_ne)

        self.radio_nevim = QRadioButton("Nevím")
        self.radio_nevim.setAccessibleName("Nevím")
        self.layout_.addWidget(self.radio_nevim)

        self.group = QButtonGroup(self)
        for r in [self.radio_ano, self.radio_ne, self.radio_nevim]:
            self.group.addButton(r)
        self.radio_nevim.setChecked(True)

        help_btn = QPushButton("Co to znamená?")
        help_btn.setAccessibleDescription("Zobrazit nápovědu")
        help_btn.setAccessibleName("Co to znamená? - vytváření EXE")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self._help_btn = help_btn
        self.layout_.addStretch()
        self.set_first_widget(self.radio_ano)

    def show_help(self):
        prev = QApplication.focusWidget()
        HelpDialog(self, "Co je vytváření EXE?",
                   "Některé nástroje umí zabalit Python program do souboru EXE, aby ho šlo spustit na Windows bez instalace Pythonu. "
                   "Například PyInstaller nebo Nuitka. Pokud nic takového neděláte, zvolte Ne.").exec()
        if prev is not None:
            QTimer.singleShot(0, prev.setFocus)

    def get_config_updates(self, config):
        if self.radio_ano.isChecked():
            config.build_answer = BuildAnswer.ANO
        elif self.radio_ne.isChecked():
            config.build_answer = BuildAnswer.NE
        else:
            config.build_answer = BuildAnswer.NEVIM

    def load_from_config(self, config):
        mapping = {BuildAnswer.ANO: self.radio_ano, BuildAnswer.NE: self.radio_ne, BuildAnswer.NEVIM: self.radio_nevim}
        mapping.get(config.build_answer, self.radio_nevim).setChecked(True)


class BuildToolPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 5b – Nástroj pro sestavení", parent)
        q = QLabel("Jaký nástroj používáte na vytváření programu?")
        q.setWordWrap(True)
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        q.setAccessibleName("Jaký nástroj používáte na vytváření programu?")
        self.layout_.addWidget(q)

        self.radio_pyinst = QRadioButton("PyInstaller")
        self.radio_pyinst.setAccessibleName("PyInstaller")
        self.radio_pyinst.setAccessibleDescription("Nástroj který vytváří EXE z Pythonu.")
        self.layout_.addWidget(self.radio_pyinst)

        self.radio_nuitka = QRadioButton("Nuitka")
        self.radio_nuitka.setAccessibleName("Nuitka")
        self.layout_.addWidget(self.radio_nuitka)

        self.radio_jiny = QRadioButton("Jiný")
        self.radio_jiny.setAccessibleName("Jiný nástroj pro sestavení")
        self.layout_.addWidget(self.radio_jiny)

        self.radio_nevim = QRadioButton("Nevím")
        self.radio_nevim.setAccessibleName("Nevím jaký nástroj pro sestavení používám")
        self.layout_.addWidget(self.radio_nevim)

        self.group = QButtonGroup(self)
        for r in [self.radio_pyinst, self.radio_nuitka, self.radio_jiny, self.radio_nevim]:
            self.group.addButton(r)
        self.radio_nevim.setChecked(True)
        self.layout_.addStretch()
        self.set_first_widget(self.radio_pyinst)

    def get_config_updates(self, config):
        if self.radio_pyinst.isChecked():
            config.build_tool = BuildTool.PYINSTALLER
        elif self.radio_nuitka.isChecked():
            config.build_tool = BuildTool.NUITKA
        elif self.radio_jiny.isChecked():
            config.build_tool = BuildTool.JINY
        else:
            config.build_tool = BuildTool.NEVIM

    def load_from_config(self, config):
        mapping = {BuildTool.PYINSTALLER: self.radio_pyinst, BuildTool.NUITKA: self.radio_nuitka, BuildTool.JINY: self.radio_jiny, BuildTool.NEVIM: self.radio_nevim}
        mapping.get(config.build_tool, self.radio_nevim).setChecked(True)
