from dataclasses import dataclass, field
from enum import Enum, auto


class ProjectType(Enum):
    PYTHON = auto()
    PYTHON_JUPYTER = auto()
    GENERIC = auto()
    UNKNOWN = auto()


class VenvChoice(Enum):
    DOT_VENV = auto()
    VENV = auto()
    ENV = auto()
    CUSTOM = auto()
    UNKNOWN = auto()


class VenvAnswer(Enum):
    ANO = auto()
    NE = auto()
    NEVIM = auto()


class TestingAnswer(Enum):
    ANO = auto()
    NE = auto()
    NEVIM = auto()


class TestingTool(Enum):
    PYTEST = auto()
    UNITTEST = auto()
    JINY = auto()
    NEVIM = auto()


class BuildAnswer(Enum):
    ANO = auto()
    NE = auto()
    NEVIM = auto()


class BuildTool(Enum):
    PYINSTALLER = auto()
    NUITKA = auto()
    JINY = auto()
    NEVIM = auto()


class IDEOption(Enum):
    VSCODE = auto()
    PYCHARM = auto()
    VISUAL_STUDIO = auto()
    SPYDER = auto()
    JINY = auto()
    NEVIM = auto()


class DataOption(Enum):
    JUPYTER = auto()
    DATASET = auto()
    TEMP = auto()
    CACHE = auto()
    LOGS = auto()
    NEVIM = auto()


class SecretOption(Enum):
    ENV = auto()
    ENV_STAR = auto()
    CONFIG_LOCAL = auto()
    CUSTOM = auto()


class SecretAnswer(Enum):
    ANO = auto()
    NE = auto()
    NEVIM = auto()


@dataclass
class CustomRule:
    pattern: str
    comment: str = ""


@dataclass
class WizardConfig:
    project_type: ProjectType = ProjectType.UNKNOWN

    venv_answer: VenvAnswer = VenvAnswer.NEVIM
    venv_choice: VenvChoice = VenvChoice.UNKNOWN
    venv_custom_name: str = ""

    ides: set = field(default_factory=set)

    testing_answer: TestingAnswer = TestingAnswer.NEVIM
    testing_tool: TestingTool = TestingTool.NEVIM

    build_answer: BuildAnswer = BuildAnswer.NEVIM
    build_tool: BuildTool = BuildTool.NEVIM

    data_options: set = field(default_factory=set)

    include_windows: bool = True

    secret_answer: SecretAnswer = SecretAnswer.NEVIM
    secret_options: set = field(default_factory=set)
    secret_custom: list = field(default_factory=list)

    custom_rules: list = field(default_factory=list)

    def resolved_venv_name(self) -> str | None:
        if self.venv_answer != VenvAnswer.ANO:
            return None
        mapping = {
            VenvChoice.DOT_VENV: ".venv",
            VenvChoice.VENV: "venv",
            VenvChoice.ENV: "env",
        }
        if self.venv_choice in mapping:
            return mapping[self.venv_choice]
        if self.venv_choice == VenvChoice.CUSTOM:
            name = self.venv_custom_name.strip()
            return name if name else None
        return None
