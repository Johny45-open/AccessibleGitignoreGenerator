from PyQt6.QtWidgets import QApplication, QRadioButton, QLabel, QPushButton, QButtonGroup, QCheckBox, QLineEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import SecretAnswer, SecretOption


class SecretsAnswerPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 7 – Tajné a místní nastavení", parent)
        q = QLabel("Obsahuje projekt místní tajné nebo soukromé nastavení?")
        q.setWordWrap(True)
        q.setAccessibleName("Obsahuje projekt místní tajné nebo soukromé nastavení?")
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_.addWidget(q)
        desc = QLabel("Například hesla, klíče nebo soubor .env s nastavením jen pro váš počítač.")
        desc.setWordWrap(True)
        self.layout_.addWidget(desc)

        self.radio_ano = QRadioButton("Ano")
        self.radio_ano.setAccessibleName("Ano – obsahuje tajné nastavení")
        self.layout_.addWidget(self.radio_ano)

        self.radio_ne = QRadioButton("Ne")
        self.radio_ne.setAccessibleName("Ne – neobsahuje tajné nastavení")
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
        help_btn.setAccessibleName("Co to znamená? - tajné soubory")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self._help_btn = help_btn
        self.layout_.addStretch()
        self.set_first_widget(self.radio_ano)

    def show_help(self):
        prev = QApplication.focusWidget()
        HelpDialog(self, "Co jsou tajné soubory?",
                   "Některé soubory obsahují hesla nebo klíče jen pro váš počítač, například .env. "
                   "Ty by neměly být v Gitu. Upozornění: .gitignore neochrání soubor, který už byl do Gitu přidán.").exec()
        if prev is not None:
            QTimer.singleShot(0, prev.setFocus)

    def get_config_updates(self, config):
        if self.radio_ano.isChecked():
            config.secret_answer = SecretAnswer.ANO
        elif self.radio_ne.isChecked():
            config.secret_answer = SecretAnswer.NE
        else:
            config.secret_answer = SecretAnswer.NEVIM

    def load_from_config(self, config):
        mapping = {SecretAnswer.ANO: self.radio_ano, SecretAnswer.NE: self.radio_ne, SecretAnswer.NEVIM: self.radio_nevim}
        mapping.get(config.secret_answer, self.radio_nevim).setChecked(True)


class SecretsOptionsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 7b – Jaké tajné soubory?", parent)
        q = QLabel("Vyberte, co chcete ignorovat:")
        q.setWordWrap(True)
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        q.setAccessibleName("Vyberte, co chcete ignorovat:")
        self.layout_.addWidget(q)

        self.cb_env = QCheckBox("Soubor s hesly (.env)")
        self.cb_env.setAccessibleName("Soubor s hesly (.env)")
        self.layout_.addWidget(self.cb_env)

        self.cb_env_star = QCheckBox("Všechny varianty (.env.*)")
        self.cb_env_star.setAccessibleName("Všechny varianty (.env.*)")
        self.layout_.addWidget(self.cb_env_star)

        self.cb_local = QCheckBox("Místní nastavení (config.local.*)")
        self.cb_local.setAccessibleName("Místní nastavení (config.local.*)")
        self.layout_.addWidget(self.cb_local)

        self.custom_label = QLabel("Vlastní cesta (volitelné):")
        self.layout_.addWidget(self.custom_label)
        self.custom_edit = QLineEdit()
        self.custom_edit.setPlaceholderText("např. secrets/config.json")
        self.custom_edit.setAccessibleName("Vlastní cesta k tajnému souboru")
        self.custom_label.setBuddy(self.custom_edit)
        self.layout_.addWidget(self.custom_edit)

        warn = QLabel("Upozornění: .gitignore nenahrazuje správu tajemství a neochrání soubor, který už byl do Gitu přidán.")
        warn.setWordWrap(True)
        warn.setStyleSheet("color: #a00;")
        warn.setAccessibleName("Upozornění: .gitignore nenahrazuje správu tajemství a neochrání soubor, který už byl do Gitu přidán.")
        self.layout_.addWidget(warn)

        self.layout_.addStretch()
        self.set_first_widget(self.cb_env)

    def get_config_updates(self, config):
        s = set()
        if self.cb_env.isChecked():
            s.add(SecretOption.ENV)
        if self.cb_env_star.isChecked():
            s.add(SecretOption.ENV_STAR)
        if self.cb_local.isChecked():
            s.add(SecretOption.CONFIG_LOCAL)
        config.secret_options = s
        custom = self.custom_edit.text().strip()
        if custom:
            config.secret_custom = [custom]
        else:
            config.secret_custom = []

    def load_from_config(self, config):
        self.cb_env.setChecked(SecretOption.ENV in config.secret_options)
        self.cb_env_star.setChecked(SecretOption.ENV_STAR in config.secret_options)
        self.cb_local.setChecked(SecretOption.CONFIG_LOCAL in config.secret_options)
        if config.secret_custom:
            self.custom_edit.setText(config.secret_custom[0])
