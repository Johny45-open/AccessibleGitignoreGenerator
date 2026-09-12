<div lang="cs">

# AccessibleGitignoreGenerator

Přístupný průvodce pro tvorbu souboru `.gitignore` pro Windows s důrazem na NVDA.

## Technologie
- Python 3.13+
- PyQt6 (pouze, žádný Tkinter/Kivy)

## Spuštění
```
pip install -r requirements.txt
python main.py
```

## Testy
```
pytest -v
```

## Architektura
- `core/models.py` – dataclass WizardConfig
- `core/generator.py` – čistá logika generování, deduplikace, komentáře
- `core/validator.py` – validace vlastních pravidel
- `templates/*.py` – oddělená datová vrstva pro snadné přidání Flutter/Rust/Node.js
- `ui/` – GUI oddělené od logiky, QStackedWidget + vlastní navigace, focus via QTimer.singleShot

## Přístupnost
- Počáteční fokus na Začít přes showEvent + QTimer.singleShot
- QGroupBox nepoužíván anonymně, každá skupina má smysluplný název
- Labels s buddy, accessibleName/Description, logický Tab order
- Help dialogy s jasným titulem a fokusem na Zavřít
- QTextEdit pro náhled čitelný NVDA

## Profily
Python, Python+Jupyter, Generic, Windows, VS Code, PyCharm, VS, Spyder, pytest, unittest, PyInstaller, Nuitka, Jupyter checkpoints, dataset, temp, cache, logy, .env, vlastní pravidla.
