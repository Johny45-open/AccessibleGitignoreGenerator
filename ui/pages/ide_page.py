from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QCheckBox, QLabel, QPushButton
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import IDEOption


class IdePage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 3 – Program na programování", parent)
        q = QLabel("V čem programujete?")
        q.setWordWrap(True)
        q.setAccessibleName("V čem programujete?")
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_.addWidget(q)
        desc = QLabel("Vyberte program, ve kterém svůj projekt upravujete.")
        desc.setWordWrap(True)
        self.layout_.addWidget(desc)

        self.cb_vscode = QCheckBox("Visual Studio Code")
        self.cb_vscode.setAccessibleName("Visual Studio Code")
        self.cb_vscode.setAccessibleDescription("Editor Visual Studio Code")
        self.layout_.addWidget(self.cb_vscode)

        self.cb_pycharm = QCheckBox("PyCharm")
        self.cb_pycharm.setAccessibleName("PyCharm")
        self.layout_.addWidget(self.cb_pycharm)

        self.cb_vs = QCheckBox("Visual Studio")
        self.cb_vs.setAccessibleName("Visual Studio")
        self.layout_.addWidget(self.cb_vs)

        self.cb_spyder = QCheckBox("Spyder")
        self.cb_spyder.setAccessibleName("Spyder")
        self.layout_.addWidget(self.cb_spyder)

        self.cb_other = QCheckBox("Jiný program")
        self.cb_other.setAccessibleName("Jiný program")
        self.layout_.addWidget(self.cb_other)

        self.cb_nevim = QCheckBox("Nevím")
        self.cb_nevim.setAccessibleName("Nevím")
        self.cb_nevim.setAccessibleDescription("Nevím v čem programuji, přeskočit")
        self.cb_nevim.toggled.connect(self.on_nevim_toggle)
        self.layout_.addWidget(self.cb_nevim)

        help_btn = QPushButton("Co to znamená?")
        help_btn.setAccessibleDescription("Zobrazit nápovědu")
        help_btn.setAccessibleName("Co to znamená? - editor")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self._help_btn = help_btn
        self.layout_.addStretch()
        self.set_first_widget(self.cb_vscode)

    def on_nevim_toggle(self, checked):
        if checked:
            for cb in [self.cb_vscode, self.cb_pycharm, self.cb_vs, self.cb_spyder, self.cb_other]:
                cb.setChecked(False)
                cb.setEnabled(False)
        else:
            for cb in [self.cb_vscode, self.cb_pycharm, self.cb_vs, self.cb_spyder, self.cb_other]:
                cb.setEnabled(True)

    def show_help(self):
        prev = QApplication.focusWidget()
        HelpDialog(self, "Co je program na programování?",
                   "Jedná se o editor nebo vývojové prostředí, například Visual Studio Code nebo PyCharm. "
                   "Tyto programy vytvářejí pomocné soubory, které obvykle nepatří do Gitu. Pokud nevíte, zvolte Nevím.").exec()
        if prev is not None:
            QTimer.singleShot(0, prev.setFocus)

    def get_config_updates(self, config):
        s = set()
        if self.cb_nevim.isChecked():
            s.add(IDEOption.NEVIM)
        else:
            if self.cb_vscode.isChecked():
                s.add(IDEOption.VSCODE)
            if self.cb_pycharm.isChecked():
                s.add(IDEOption.PYCHARM)
            if self.cb_vs.isChecked():
                s.add(IDEOption.VISUAL_STUDIO)
            if self.cb_spyder.isChecked():
                s.add(IDEOption.SPYDER)
            if self.cb_other.isChecked():
                s.add(IDEOption.JINY)
        config.ides = s

    def load_from_config(self, config):
        self.cb_vscode.setChecked(IDEOption.VSCODE in config.ides)
        self.cb_pycharm.setChecked(IDEOption.PYCHARM in config.ides)
        self.cb_vs.setChecked(IDEOption.VISUAL_STUDIO in config.ides)
        self.cb_spyder.setChecked(IDEOption.SPYDER in config.ides)
        self.cb_other.setChecked(IDEOption.JINY in config.ides)
        self.cb_nevim.setChecked(IDEOption.NEVIM in config.ides)
