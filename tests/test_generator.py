import sys
sys.path.insert(0, "C:\\Honza\\Projekty\\AccessibleGitignoreGenerator")

from core.models import (
    WizardConfig, ProjectType, VenvAnswer, VenvChoice, IDEOption,
    TestingAnswer, TestingTool, BuildAnswer, BuildTool, DataOption, SecretAnswer, SecretOption, CustomRule
)
from core.generator import generate


def test_python_only():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, include_windows=False)
    out = generate(cfg)
    assert "__pycache__/" in out
    assert "*.py[cod]" in out
    assert "Thumbs.db" not in out


def test_python_vscode():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, ides={IDEOption.VSCODE})
    out = generate(cfg)
    assert ".vscode/" in out
    assert "__pycache__/" in out


def test_python_pytest():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, testing_answer=TestingAnswer.ANO, testing_tool=TestingTool.PYTEST)
    out = generate(cfg)
    assert ".pytest_cache/" in out


def test_python_pyinstaller():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, build_answer=BuildAnswer.ANO, build_tool=BuildTool.PYINSTALLER)
    out = generate(cfg)
    assert "*.spec" in out


def test_python_windows_vscode():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, ides={IDEOption.VSCODE}, include_windows=True)
    out = generate(cfg)
    assert "Thumbs.db" in out
    assert ".vscode/" in out
    assert "__pycache__/" in out


def test_dedup():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, ides={IDEOption.VSCODE, IDEOption.PYCHARM},
                       data_options={DataOption.CACHE}, include_windows=True)
    out = generate(cfg)
    # __pycache__/ should appear only once even if multiple profiles would add
    assert out.count("__pycache__/") == 1


def test_custom_rules():
    cfg = WizardConfig(project_type=ProjectType.GENERIC, include_windows=False,
                       custom_rules=[CustomRule("secrets/", ""), CustomRule("my_local_data/", "moje data")])
    out = generate(cfg)
    assert "secrets/" in out
    assert "my_local_data/" in out
    assert "moje data" in out


def test_nevim_conservative():
    cfg = WizardConfig(project_type=ProjectType.UNKNOWN, testing_answer=TestingAnswer.NEVIM, build_answer=BuildAnswer.NEVIM,
                       venv_answer=VenvAnswer.NEVIM, ides={IDEOption.NEVIM}, data_options={DataOption.NEVIM})
    out = generate(cfg)
    # Should not contain python specific if unknown
    assert "__pycache__/" not in out
    # Windows still by default
    assert "Thumbs.db" in out
    # No testing/build
    assert ".pytest_cache/" not in out


def test_testing_ano_nevim_no_pytest():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, testing_answer=TestingAnswer.ANO, testing_tool=TestingTool.NEVIM)
    out = generate(cfg)
    assert ".pytest_cache/" not in out


def test_build_nevim_no_pyinstaller():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, build_answer=BuildAnswer.ANO, build_tool=BuildTool.NEVIM)
    out = generate(cfg)
    assert "*.spec" not in out


def test_venv():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, venv_answer=VenvAnswer.ANO, venv_choice=VenvChoice.DOT_VENV, include_windows=False)
    out = generate(cfg)
    assert ".venv/" in out

    cfg2 = WizardConfig(project_type=ProjectType.PYTHON, venv_answer=VenvAnswer.ANO, venv_choice=VenvChoice.CUSTOM, venv_custom_name="myenv", include_windows=False)
    out2 = generate(cfg2)
    assert "myenv/" in out2


def test_venv_nevim_no_add():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, venv_answer=VenvAnswer.NEVIM, include_windows=False)
    out = generate(cfg)
    assert ".venv/" not in out
    assert "venv/" not in out


def test_comments_grouped():
    cfg = WizardConfig(project_type=ProjectType.PYTHON, ides={IDEOption.VSCODE}, include_windows=True)
    out = generate(cfg)
    assert "# Python" in out
    assert "# VS Code" in out
    assert "# Windows" in out


def test_empty_custom_rule_not_added():
    cfg = WizardConfig(project_type=ProjectType.GENERIC, include_windows=False, custom_rules=[CustomRule("   ", "")])
    out = generate(cfg)
    # Should not crash, empty rule ignored
    assert "   " not in out or out.strip() != ""
