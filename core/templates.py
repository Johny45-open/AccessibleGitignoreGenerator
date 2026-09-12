from templates.python import TEMPLATE as PYTHON_TPL
from templates.windows import TEMPLATE as WINDOWS_TPL
from templates.vscode import TEMPLATE as VSCODE_TPL
from templates.pycharm import TEMPLATE as PYCHARM_TPL
from templates.visualstudio import TEMPLATE as VS_TPL
from templates.spyder import TEMPLATE as SPYDER_TPL
from templates.pytest import TEMPLATE as PYTEST_TPL
from templates.unittest_tpl import TEMPLATE as UNITTEST_TPL
from templates.pyinstaller import TEMPLATE as PYINSTALLER_TPL
from templates.nuitka import TEMPLATE as NUITKA_TPL
from templates.jupyter import JUPYTER_RULES, DATASET_RULES, TEMP_RULES, CACHE_RULES, LOGS_RULES
from templates.secrets import TEMPLATE_ENV, TEMPLATE_ENV_STAR, TEMPLATE_CONFIG_LOCAL

REGISTRY = {
    "python": PYTHON_TPL,
    "windows": WINDOWS_TPL,
    "vscode": VSCODE_TPL,
    "pycharm": PYCHARM_TPL,
    "visualstudio": VS_TPL,
    "spyder": SPYDER_TPL,
    "pytest": PYTEST_TPL,
    "unittest": UNITTEST_TPL,
    "pyinstaller": PYINSTALLER_TPL,
    "nuitka": NUITKA_TPL,
    "jupyter": {"header": "Jupyter Notebook", "rules": JUPYTER_RULES},
    "dataset": DATASET_RULES,
    "temp": TEMP_RULES,
    "cache": CACHE_RULES,
    "logs": LOGS_RULES,
    "env": TEMPLATE_ENV,
    "env_star": TEMPLATE_ENV_STAR,
    "config_local": TEMPLATE_CONFIG_LOCAL,
}
