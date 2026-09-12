from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QRadioButton, QLabel, QPushButton, QButtonGroup
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import TestingAnswer, TestingTool


class TestingAnswerPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 4 – Automatické testy", parent)
        q = QLabel("Používáte automatické testy, které kontrolují váš program?")
        q.setWordWrap(True)
        q.setAccessibleName("Používáte automatické testy, které kontrolují váš program?")
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_.addWidget(q)
        desc = QLabel("Nástroj, který automaticky kontroluje, zda části vašeho programu fungují správně.")
        desc.setWordWrap(True)
        self.layout_.addWidget(desc)

        self.radio_ano = QRadioButton("Ano")
        self.radio_ano.setAccessibleName("Ano – používám automatické testy")
        self.layout_.addWidget(self.radio_ano)

        self.radio_ne = QRadioButton("Ne")
        self.radio_ne.setAccessibleName("Ne – nepoužívám automatické testy")
        self.layout_.addWidget(self.radio_ne)

        self.radio_nevim = QRadioButton("Nevím")
        self.radio_nevim.setAccessibleName("Nevím")
        self.radio_nevim.setAccessibleDescription("Nevím zda používám automatické testy")
        self.layout_.addWidget(self.radio_nevim)

        self.group = QButtonGroup(self)
        for r in [self.radio_ano, self.radio_ne, self.radio_nevim]:
            self.group.addButton(r)
        self.radio_nevim.setChecked(True)

        help_btn = QPushButton("Co to znamená?")
        help_btn.setAccessibleDescription("Zobrazit nápovědu")
        help_btn.setAccessibleName("Co to znamená? - automatické testy")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self._help_btn = help_btn
        self.layout_.addStretch()
        self.set_first_widget(self.radio_ano)

    def show_help(self):
        prev = QApplication.focusWidget()
        HelpDialog(self, "Co jsou automatické testy?",
                   "Automatické testy jsou programy, které samy kontrolují, zda váš program dělá to, co má. "
                   "Pytest je jeden z nástrojů, který se pro tyto testy v Pythonu používá.").exec()
        if prev is not None:
            QTimer.singleShot(0, prev.setFocus)

    def get_config_updates(self, config):
        if self.radio_ano.isChecked():
            config.testing_answer = TestingAnswer.ANO
        elif self.radio_ne.isChecked():
            config.testing_answer = TestingAnswer.NE
        else:
            config.testing_answer = TestingAnswer.NEVIM

    def load_from_config(self, config):
        mapping = {TestingAnswer.ANO: self.radio_ano, TestingAnswer.NE: self.radio_ne, TestingAnswer.NEVIM: self.radio_nevim}
        mapping.get(config.testing_answer, self.radio_nevim).setChecked(True)


class TestingToolPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 4b – Nástroj na testy", parent)
        q = QLabel("Který nástroj používáte na testy?")
        q.setWordWrap(True)
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        q.setAccessibleName("Který nástroj používáte na testy?")
        self.layout_.addWidget(q)

        self.radio_pytest = QRadioButton("Automatické testy (pytest)")
        self.radio_pytest.setAccessibleName("Automatické testy (pytest)")
        self.radio_pytest.setAccessibleDescription("Nástroj, který automaticky kontroluje, zda části vašeho programu fungují správně.")
        self.layout_.addWidget(self.radio_pytest)
        lbl1 = QLabel("Nástroj, který automaticky kontroluje, zda části vašeho programu fungují správně.")
        lbl1.setWordWrap(True)
        self.layout_.addWidget(lbl1)

        self.radio_unittest = QRadioButton("Automatické testy (unittest)")
        self.radio_unittest.setAccessibleName("Automatické testy (unittest)")
        self.radio_unittest.setAccessibleDescription("Zabudovaný nástroj Pythonu na testování.")
        self.layout_.addWidget(self.radio_unittest)

        self.radio_jiny = QRadioButton("Jiný")
        self.radio_jiny.setAccessibleName("Jiný nástroj na testy")
        self.layout_.addWidget(self.radio_jiny)

        self.radio_nevim = QRadioButton("Nevím")
        self.radio_nevim.setAccessibleName("Nevím jaký nástroj na testy používám")
        self.layout_.addWidget(self.radio_nevim)

        self.group = QButtonGroup(self)
        for r in [self.radio_pytest, self.radio_unittest, self.radio_jiny, self.radio_nevim]:
            self.group.addButton(r)
        self.radio_nevim.setChecked(True)
        self.layout_.addStretch()
        self.set_first_widget(self.radio_pytest)

    def get_config_updates(self, config):
        if self.radio_pytest.isChecked():
            config.testing_tool = TestingTool.PYTEST
        elif self.radio_unittest.isChecked():
            config.testing_tool = TestingTool.UNITTEST
        elif self.radio_jiny.isChecked():
            config.testing_tool = TestingTool.JINY
        else:
            config.testing_tool = TestingTool.NEVIM

    def load_from_config(self, config):
        mapping = {TestingTool.PYTEST: self.radio_pytest, TestingTool.UNITTEST: self.radio_unittest, TestingTool.JINY: self.radio_jiny, TestingTool.NEVIM: self.radio_nevim}
        mapping.get(config.testing_tool, self.radio_nevim).setChecked(True)
