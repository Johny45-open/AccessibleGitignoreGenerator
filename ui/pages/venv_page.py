from PyQt6.QtWidgets import QRadioButton, QLabel, QPushButton, QButtonGroup, QComboBox, QLineEdit, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import VenvAnswer, VenvChoice


class VenvAnswerPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 2 – Prostředí Pythonu", parent)
        q = QLabel("Má tento projekt vlastní oddělené prostředí pro Python balíčky?")
        q.setWordWrap(True)
        q.setAccessibleName("Má tento projekt vlastní oddělené prostředí pro Python balíčky?")
        self.layout_.addWidget(q)
        desc = QLabel("Virtuální prostředí umožňuje mít pro každý projekt samostatné verze balíčků.")
        desc.setWordWrap(True)
        self.layout_.addWidget(desc)

        self.radio_ano = QRadioButton("Ano")
        self.radio_ano.setAccessibleName("Ano – má vlastní prostředí")
        self.radio_ano.setAccessibleDescription("Projekt má vlastní oddělené prostředí.")
        self.layout_.addWidget(self.radio_ano)

        self.radio_ne = QRadioButton("Ne")
        self.radio_ne.setAccessibleName("Ne – nemá vlastní prostředí")
        self.layout_.addWidget(self.radio_ne)

        self.radio_nevim = QRadioButton("Nevím")
        self.radio_nevim.setAccessibleName("Nevím")
        self.radio_nevim.setAccessibleDescription("Nevím zda projekt má vlastní prostředí.")
        self.layout_.addWidget(self.radio_nevim)

        self.group = QButtonGroup(self)
        for r in [self.radio_ano, self.radio_ne, self.radio_nevim]:
            self.group.addButton(r)
        self.radio_nevim.setChecked(True)

        help_btn = QPushButton("Co to znamená?")
        help_btn.setAccessibleName("Co to znamená? - virtuální prostředí")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self.layout_.addStretch()
        self.set_first_widget(self.radio_ano)

    def show_help(self):
        HelpDialog(self, "Co je virtuální prostředí?",
                   "Virtuální prostředí je složka, kde má projekt vlastní kopie Python balíčků. "
                   "Běžné názvy jsou .venv nebo venv. Pokud nevíte, zvolte Nevím – nic se nepřidá.").exec()

    def get_config_updates(self, config):
        if self.radio_ano.isChecked():
            config.venv_answer = VenvAnswer.ANO
        elif self.radio_ne.isChecked():
            config.venv_answer = VenvAnswer.NE
        else:
            config.venv_answer = VenvAnswer.NEVIM

    def load_from_config(self, config):
        mapping = {VenvAnswer.ANO: self.radio_ano, VenvAnswer.NE: self.radio_ne, VenvAnswer.NEVIM: self.radio_nevim}
        mapping.get(config.venv_answer, self.radio_nevim).setChecked(True)


class VenvNamePage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 2b – Název prostředí", parent)
        q = QLabel("Jak se vaše virtuální prostředí jmenuje?")
        q.setWordWrap(True)
        q.setAccessibleName("Jak se vaše virtuální prostředí jmenuje?")
        self.layout_.addWidget(q)

        self.combo = QComboBox()
        self.combo.setAccessibleName("Název virtuálního prostředí")
        self.combo.setAccessibleDescription("Vyberte název složky prostředí")
        self.combo.addItems([".venv (doporučeno)", "venv", "env", "jiný název", "nevím"])
        self.combo.currentTextChanged.connect(self.on_combo_change)
        self.layout_.addWidget(self.combo)

        self.custom_edit = QLineEdit()
        self.custom_edit.setPlaceholderText("zadejte vlastní název, např. myenv")
        self.custom_edit.setAccessibleName("Vlastní název prostředí")
        self.custom_edit.setEnabled(False)
        self.layout_.addWidget(QLabel("Vlastní název:"))
        self.layout_.addWidget(self.custom_edit)

        self.layout_.addStretch()
        self.set_first_widget(self.combo)

    def on_combo_change(self, text):
        is_custom = "jiný název" in text
        self.custom_edit.setEnabled(is_custom)
        if is_custom:
            self.custom_edit.setFocus()

    def get_config_updates(self, config):
        txt = self.combo.currentText()
        if "nevím" in txt:
            config.venv_choice = VenvChoice.UNKNOWN
        elif ".venv" in txt:
            config.venv_choice = VenvChoice.DOT_VENV
        elif txt == "venv":
            config.venv_choice = VenvChoice.VENV
        elif txt == "env":
            config.venv_choice = VenvChoice.ENV
        elif "jiný" in txt:
            config.venv_choice = VenvChoice.CUSTOM
            config.venv_custom_name = self.custom_edit.text().strip()
        else:
            config.venv_choice = VenvChoice.UNKNOWN

    def load_from_config(self, config):
        mapping = {
            VenvChoice.DOT_VENV: 0,
            VenvChoice.VENV: 1,
            VenvChoice.ENV: 2,
            VenvChoice.CUSTOM: 3,
            VenvChoice.UNKNOWN: 4,
        }
        idx = mapping.get(config.venv_choice, 0)
        self.combo.setCurrentIndex(idx)
        if config.venv_choice == VenvChoice.CUSTOM:
            self.custom_edit.setText(config.venv_custom_name)

    def validate_page(self):
        txt = self.combo.currentText()
        if "jiný" in txt and not self.custom_edit.text().strip():
            return "Zadejte vlastní název prostředí nebo zvolte jinou možnost."
        return None
