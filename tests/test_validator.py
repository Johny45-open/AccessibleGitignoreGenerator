import sys
sys.path.insert(0, "C:\\Honza\\Projekty\\AccessibleGitignoreGenerator")

from core.validator import validate_custom_rule, validate_venv_name


def test_empty_rule():
    assert validate_custom_rule("") is not None
    assert validate_custom_rule("   ") is not None


def test_valid_rule():
    assert validate_custom_rule("secrets/") is None
    assert validate_custom_rule("*.log") is None


def test_absolute_path():
    assert validate_custom_rule("C:\\secrets") is not None
    assert validate_custom_rule("D:/data") is not None


def test_duplicate():
    assert validate_custom_rule("a", ["a", "b"]) is not None
    assert validate_custom_rule("c", ["a", "b"]) is None


def test_venv_valid():
    assert validate_venv_name(".venv") is None
    assert validate_venv_name("myenv") is None


def test_venv_empty():
    assert validate_venv_name("") is not None
    assert validate_venv_name("   ") is not None


def test_venv_slash():
    assert validate_venv_name("a/b") is not None
