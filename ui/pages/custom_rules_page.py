from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox
from ui.pages.base_page import BasePage
from ui.dialogs import CustomRuleDialog
from core.models import CustomRule


class CustomRulesPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 8 – Vlastní pravidla", parent)
        desc = QLabel("Můžete přidat vlastní pravidla, která nejsou v průvodci. Například: secrets/ nebo my_local_data/")
        desc.setWordWrap(True)
        desc.setAccessibleName("Můžete přidat vlastní pravidla, která nejsou v průvodci.")
        self.layout_.addWidget(desc)

        self.list_widget = QListWidget()
        self.list_widget.setAccessibleName("Seznam vlastních pravidel")
        self.list_widget.setAccessibleDescription("Seznam vlastních pravidel, která budou přidána do .gitignore")
        self.layout_.addWidget(self.list_widget)

        btn_row = QWidget()
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_add = QPushButton("Přidat vlastní pravidlo")
        self.btn_add.setAccessibleName("Přidat vlastní pravidlo")
        self.btn_add.clicked.connect(self.on_add)
        btn_row_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Odebrat vybrané")
        self.btn_remove.setAccessibleName("Odebrat vybrané pravidlo")
        self.btn_remove.clicked.connect(self.on_remove)
        btn_row_layout.addWidget(self.btn_remove)
        btn_row_layout.addStretch()
        self.layout_.addWidget(btn_row)

        self._rules: list[CustomRule] = []
        self.layout_.addStretch()
        self.set_first_widget(self.btn_add)

    def on_add(self):
        existing = [r.pattern for r in self._rules]
        dlg = CustomRuleDialog(self, existing)
        if dlg.exec() == CustomRuleDialog.DialogCode.Accepted:
            pattern, comment = dlg.get_data()
            rule = CustomRule(pattern=pattern, comment=comment)
            self._rules.append(rule)
            display = f"{pattern}" + (f"  # {comment}" if comment else "")
            self.list_widget.addItem(display)
            self.list_widget.setCurrentRow(self.list_widget.count() - 1)

    def on_remove(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)
            del self._rules[row]
        else:
            QMessageBox.information(self, "Informace", "Vyberte pravidlo k odebrání.")

    def get_config_updates(self, config):
        config.custom_rules = list(self._rules)

    def load_from_config(self, config):
        self._rules = list(config.custom_rules)
        self.list_widget.clear()
        for r in self._rules:
            display = f"{r.pattern}" + (f"  # {r.comment}" if r.comment else "")
            self.list_widget.addItem(display)
