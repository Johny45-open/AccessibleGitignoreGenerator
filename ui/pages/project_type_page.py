from PyQt6.QtWidgets import QRadioButton, QLabel, QPushButton, QButtonGroup
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import ProjectType


class ProjectTypePage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 1 – Typ projektu", parent)
        q = QLabel("Jaký typ projektu vytváříte?")
        q.setWordWrap(True)
        q.setAccessibleName("Jaký typ projektu vytváříte?")
        self.layout_.addWidget(q)

        self.radio_python = QRadioButton("Python projekt")
        self.radio_python.setAccessibleName("Python projekt")
        self.radio_python.setAccessibleDescription("Program nebo skript psaný v jazyce Python.")
        self.layout_.addWidget(self.radio_python)
        lbl1 = QLabel("Program nebo skript psaný v jazyce Python.")
        lbl1.setWordWrap(True)
        lbl1.setAccessibleName("Program nebo skript psaný v jazyce Python.")
        self.layout_.addWidget(lbl1)

        self.radio_jupyter = QRadioButton("Python s interaktivními dokumenty (Python + Jupyter)")
        self.radio_jupyter.setAccessibleName("Python s interaktivními dokumenty (Python + Jupyter)")
        self.radio_jupyter.setAccessibleDescription("Python doplněný o dokumenty kde je text, kód a výsledky pohromadě.")
        self.layout_.addWidget(self.radio_jupyter)
        lbl2 = QLabel("Python doplněný o dokumenty kde je text, kód a výsledky pohromadě. Například Jupyter Notebook.")
        lbl2.setWordWrap(True)
        self.layout_.addWidget(lbl2)

        self.radio_generic = QRadioButton("Obecný projekt")
        self.radio_generic.setAccessibleName("Obecný projekt")
        self.radio_generic.setAccessibleDescription("Projekt bez specifického jazyka.")
        self.layout_.addWidget(self.radio_generic)

        self.radio_unknown = QRadioButton("Nevím")
        self.radio_unknown.setAccessibleName("Nevím")
        self.radio_unknown.setAccessibleDescription("Nevím jaký typ projektu to je.")
        self.layout_.addWidget(self.radio_unknown)

        self.group = QButtonGroup(self)
        for r in [self.radio_python, self.radio_jupyter, self.radio_generic, self.radio_unknown]:
            self.group.addButton(r)

        self.radio_python.setChecked(True)

        help_btn = QPushButton("Co to znamená?")
        help_btn.setAccessibleName("Co to znamená? - typ projektu")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self.layout_.addStretch()
        self.set_first_widget(self.radio_python)

    def show_help(self):
        dlg = HelpDialog(self, "Co je typ projektu?",
                         "Typ projektu určuje základní nastavení. Pokud tvoříte program v Pythonu, vyberte Python. "
                         "Pokud navíc používáte interaktivní dokumenty Jupyter Notebook, vyberte Python + Jupyter. "
                         "Pokud nevíte, zvolte Nevím – vytvoří se bezpečný obecný soubor.")
        dlg.exec()

    def get_config_updates(self, config):
        if self.radio_python.isChecked():
            config.project_type = ProjectType.PYTHON
        elif self.radio_jupyter.isChecked():
            config.project_type = ProjectType.PYTHON_JUPYTER
        elif self.radio_generic.isChecked():
            config.project_type = ProjectType.GENERIC
        else:
            config.project_type = ProjectType.UNKNOWN

    def load_from_config(self, config):
        mapping = {
            ProjectType.PYTHON: self.radio_python,
            ProjectType.PYTHON_JUPYTER: self.radio_jupyter,
            ProjectType.GENERIC: self.radio_generic,
            ProjectType.UNKNOWN: self.radio_unknown,
        }
        mapping.get(config.project_type, self.radio_python).setChecked(True)
