from core.models import (
    WizardConfig, ProjectType, VenvAnswer, TestingAnswer, TestingTool,
    BuildAnswer, BuildTool, IDEOption, DataOption, SecretAnswer, SecretOption
)
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


def generate(config: WizardConfig) -> str:
    sections: list[tuple[str, list[str]]] = []
    seen: set[str] = set()

    def add_section(header: str, rules: list[str]):
        # deduplicate within and across sections
        unique = []
        for r in rules:
            r = r.strip()
            if not r:
                continue
            if r not in seen:
                seen.add(r)
                unique.append(r)
        if unique:
            sections.append((header, unique))

    # Python base - only if python or python+jupyter
    if config.project_type in (ProjectType.PYTHON, ProjectType.PYTHON_JUPYTER):
        add_section(PYTHON_TPL["header"], PYTHON_TPL["rules"])

    # Jupyter checkpoints if python+jupyter or data option jupyter
    if config.project_type == ProjectType.PYTHON_JUPYTER or DataOption.JUPYTER in config.data_options:
        add_section("Jupyter Notebook", JUPYTER_RULES)

    # venv
    venv_name = config.resolved_venv_name()
    if venv_name:
        # ensure trailing slash
        pattern = venv_name if venv_name.endswith("/") else venv_name + "/"
        add_section("Virtualni prostredi", [pattern])

    # Windows
    if config.include_windows:
        add_section(WINDOWS_TPL["header"], WINDOWS_TPL["rules"])

    # IDEs
    if IDEOption.NEVIM not in config.ides:
        if IDEOption.VSCODE in config.ides:
            add_section(VSCODE_TPL["header"], VSCODE_TPL["rules"])
        if IDEOption.PYCHARM in config.ides:
            add_section(PYCHARM_TPL["header"], PYCHARM_TPL["rules"])
        if IDEOption.VISUAL_STUDIO in config.ides:
            add_section(VS_TPL["header"], VS_TPL["rules"])
        if IDEOption.SPYDER in config.ides:
            add_section(SPYDER_TPL["header"], SPYDER_TPL["rules"])

    # Testing
    if config.testing_answer == TestingAnswer.ANO:
        if config.testing_tool == TestingTool.PYTEST:
            add_section(PYTEST_TPL["header"], PYTEST_TPL["rules"])
        elif config.testing_tool == TestingTool.UNITTEST:
            add_section(UNITTEST_TPL["header"], UNITTEST_TPL["rules"])
        elif config.testing_tool == TestingTool.JINY:
            # generic testing cache
            add_section("Testy", [".coverage", "htmlcov/"])
        # NEVIM -> no section

    # Build
    if config.build_answer == BuildAnswer.ANO:
        if config.build_tool == BuildTool.PYINSTALLER:
            add_section(PYINSTALLER_TPL["header"], PYINSTALLER_TPL["rules"])
        elif config.build_tool == BuildTool.NUITKA:
            add_section(NUITKA_TPL["header"], NUITKA_TPL["rules"])
        elif config.build_tool == BuildTool.JINY:
            add_section("Build", ["build/", "dist/"])
        # NEVIM -> nothing

    # Data options
    if DataOption.NEVIM not in config.data_options:
        if DataOption.DATASET in config.data_options:
            add_section(DATASET_RULES["header"], DATASET_RULES["rules"])
        if DataOption.TEMP in config.data_options:
            add_section(TEMP_RULES["header"], TEMP_RULES["rules"])
        if DataOption.CACHE in config.data_options:
            add_section(CACHE_RULES["header"], CACHE_RULES["rules"])
        if DataOption.LOGS in config.data_options:
            add_section(LOGS_RULES["header"], LOGS_RULES["rules"])

    # Secrets
    if config.secret_answer == SecretAnswer.ANO:
        if SecretOption.ENV in config.secret_options:
            add_section(TEMPLATE_ENV["header"], TEMPLATE_ENV["rules"])
        if SecretOption.ENV_STAR in config.secret_options:
            add_section(TEMPLATE_ENV_STAR["header"], TEMPLATE_ENV_STAR["rules"])
        if SecretOption.CONFIG_LOCAL in config.secret_options:
            add_section(TEMPLATE_CONFIG_LOCAL["header"], TEMPLATE_CONFIG_LOCAL["rules"])
        for custom in config.secret_custom:
            c = custom.strip()
            if c and c not in seen:
                # add as single rule section grouped
                # we collect all customs into one section
                pass
        if config.secret_custom:
            customs = [c.strip() for c in config.secret_custom if c.strip() and c.strip() not in seen]
            # need to check seen again after filtering
            unique_customs = []
            for c in customs:
                if c not in seen:
                    seen.add(c)
                    unique_customs.append(c)
            if unique_customs:
                add_section("Tajne soubory - vlastni", unique_customs)

    # Custom rules
    if config.custom_rules:
        customs = []
        for r in config.custom_rules:
            pat = r.pattern.strip() if hasattr(r, 'pattern') else str(r).strip()
            comment = getattr(r, 'comment', '')
            if pat and pat not in seen:
                seen.add(pat)
                if comment and comment.strip():
                    customs.append(f"# {comment.strip()}")
                customs.append(pat)
        if customs:
            # For custom, we want to preserve comments interleaved
            # Add as one section but handle already deduped
            # Re-add logic: we already handled, just append section
            # To avoid double header, we reconstruct:
            # Remove last added if it was custom? Instead just add directly
            sections.append(("Vlastni pravidla", customs))
            # But we already added seen, so need to not duplicate header logic
            # The above adds header again, but we used seen already
            # So we need to undo duplicate handling - simpler: if we added via add_section we lose comments
            # So we keep this as is (comments preserved)
            pass

    # Build text
    lines: list[str] = []
    lines.append("# .gitignore vygenerovany pomoci AccessibleGitignoreGenerator")
    lines.append("# https://github.com/AccessibleGitignoreGenerator")
    lines.append("")

    for header, rules in sections:
        # Avoid duplicate header if last section was same header due to custom handling
        # sections already contain correct headers
        lines.append(f"# {header}")
        for r in rules:
            lines.append(r)
        lines.append("")

    result = "\n".join(lines).strip() + "\n"
    return result
