from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QCheckBox, QLabel, QPushButton
from ui.pages.base_page import BasePage
from ui.dialogs import HelpDialog
from core.models import DataOption


class DataPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("Krok 6 – Data a pomocné soubory", parent)
        q = QLabel("Co všechno váš projekt používá nebo vytváří? Zaškrtněte co platí.")
        q.setWordWrap(True)
        q.setAccessibleName("Co všechno váš projekt používá nebo vytváří?")
        q.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_.addWidget(q)

        self.cb_jupyter = QCheckBox("Interaktivní dokumenty (Jupyter Notebook)")
        self.cb_jupyter.setAccessibleName("Interaktivní dokumenty (Jupyter Notebook)")
        self.cb_jupyter.setAccessibleDescription("Dokumenty kde je text, kód a výsledky pohromadě, například Jupyter Notebook.")
        self.layout_.addWidget(self.cb_jupyter)
        lbl_j = QLabel("Dokumenty kde je text, programový kód a jeho výsledky pohromadě. Například Jupyter Notebook.")
        lbl_j.setWordWrap(True)
        self.layout_.addWidget(lbl_j)

        self.cb_dataset = QCheckBox("Místní data a datasety (data/, dataset/)")
        self.cb_dataset.setAccessibleName("Místní data a datasety")
        self.layout_.addWidget(self.cb_dataset)

        self.cb_temp = QCheckBox("Dočasné soubory")
        self.cb_temp.setAccessibleName("Dočasné soubory")
        self.layout_.addWidget(self.cb_temp)

        self.cb_cache = QCheckBox("Mezipaměť (cache)")
        self.cb_cache.setAccessibleName("Mezipaměť (cache)")
        self.cb_cache.setAccessibleDescription("Uložené dočasné výsledky pro zrychlení.")
        self.layout_.addWidget(self.cb_cache)

        self.cb_logs = QCheckBox("Záznamy běhu (logy)")
        self.cb_logs.setAccessibleName("Záznamy běhu (logy)")
        self.layout_.addWidget(self.cb_logs)

        self.cb_aiml = QCheckBox("AI / Machine Learning modely (EasyOCR, PyTorch, ONNX)")
        self.cb_aiml.setAccessibleName("AI / Machine Learning modely")
        self.cb_aiml.setAccessibleDescription(
            "Lokálně stažené nebo generované modely, váhy a checkpointy: *.pth, *.pt, *.onnx, *.ckpt, *.safetensors, .EasyOCR/. "
            "Volitelné, nezaškrtávejte pokud mají být modely součástí repozitáře."
        )
        self.layout_.addWidget(self.cb_aiml)
        lbl_aiml = QLabel(
            "Lokální modely a váhy stahované za běhu, například EasyOCR (.EasyOCR/), PyTorch (*.pth, *.pt, *.ckpt) nebo ONNX (*.onnx, *.safetensors). "
            "Neignoruje obecné složky jako models/."
        )
        lbl_aiml.setWordWrap(True)
        self.layout_.addWidget(lbl_aiml)

        self.cb_nevim = QCheckBox("Nevím – přeskočit tuto část")
        self.cb_nevim.setAccessibleName("Nevím – přeskočit tuto část")
        self.cb_nevim.toggled.connect(self.on_nevim)
        self.layout_.addWidget(self.cb_nevim)

        help_btn = QPushButton("Vysvětlit")
        help_btn.setAccessibleDescription("Zobrazit nápovědu")
        help_btn.setAccessibleName("Vysvětlit - data a cache")
        help_btn.clicked.connect(self.show_help)
        self.layout_.addWidget(help_btn)
        self._help_btn = help_btn
        self.layout_.addStretch()
        self.set_first_widget(self.cb_jupyter)

    def on_nevim(self, checked):
        for cb in [self.cb_jupyter, self.cb_dataset, self.cb_temp, self.cb_cache, self.cb_logs, self.cb_aiml]:
            if checked:
                cb.setChecked(False)
                cb.setEnabled(False)
            else:
                cb.setEnabled(True)

    def show_help(self):
        prev = QApplication.focusWidget()
        HelpDialog(self, "Co jsou data a cache?",
                   "Některé projekty pracují s velkými daty, dočasnými soubory nebo záznamy běhu (logy). "
                   "Mezipaměť (cache) jsou dočasně uložené výsledky pro zrychlení. Většinou tyto soubory do Gitu nepatří.\n\n"
                   "AI / Machine Learning modely: lokálně stažené nebo generované váhy a checkpointy "
                   "(EasyOCR ukládá modely do .EasyOCR/, PyTorch používá *.pth, *.pt, *.ckpt, ONNX *.onnx, Hugging Face *.safetensors). "
                   "Tento profil je volitelný – nezaškrtávejte jej, pokud mají být modely součástí repozitáře. "
                   "Neobsahuje obecné pravidlo models/, aby neignoroval legitimní zdrojové soubory.").exec()
        if prev is not None:
            QTimer.singleShot(0, prev.setFocus)

    def get_config_updates(self, config):
        s = set()
        if self.cb_nevim.isChecked():
            s.add(DataOption.NEVIM)
        else:
            if self.cb_jupyter.isChecked():
                s.add(DataOption.JUPYTER)
            if self.cb_dataset.isChecked():
                s.add(DataOption.DATASET)
            if self.cb_temp.isChecked():
                s.add(DataOption.TEMP)
            if self.cb_cache.isChecked():
                s.add(DataOption.CACHE)
            if self.cb_logs.isChecked():
                s.add(DataOption.LOGS)
            if self.cb_aiml.isChecked():
                s.add(DataOption.AI_ML)
        config.data_options = s

    def load_from_config(self, config):
        self.cb_jupyter.setChecked(DataOption.JUPYTER in config.data_options)
        self.cb_dataset.setChecked(DataOption.DATASET in config.data_options)
        self.cb_temp.setChecked(DataOption.TEMP in config.data_options)
        self.cb_cache.setChecked(DataOption.CACHE in config.data_options)
        self.cb_logs.setChecked(DataOption.LOGS in config.data_options)
        self.cb_aiml.setChecked(DataOption.AI_ML in config.data_options)
        self.cb_nevim.setChecked(DataOption.NEVIM in config.data_options)
