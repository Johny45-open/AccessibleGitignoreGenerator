import re
import os


def validate_custom_rule(pattern: str, existing_patterns: list[str] | None = None) -> str | None:
    """Return error message or None if valid."""
    if pattern is None or pattern.strip() == "":
        return "Pravidlo nesmí být prázdné."
    stripped = pattern.strip()
    if len(stripped) > 500:
        return "Pravidlo je příliš dlouhé."
    # Check absolute Windows path
    if re.match(r"^[a-zA-Z]:[\\/]", stripped):
        return "Pravidlo nesmí být absolutní cesta Windows (např. C:\\...). Použijte relativní cestu."
    if stripped.startswith("\\\\"):
        return "Pravidlo nesmí být síťová cesta (\\\\...)."
    if existing_patterns and stripped in existing_patterns:
        return "Toto pravidlo již existuje."
    # Invalid characters check - allow typical gitignore syntax
    # Empty validation done, otherwise allow
    return None


def validate_venv_name(name: str) -> str | None:
    if not name or name.strip() == "":
        return "Název prostředí nesmí být prázdný."
    stripped = name.strip()
    if "/" in stripped or "\\" in stripped:
        return "Název nesmí obsahovat lomítka."
    if len(stripped) > 100:
        return "Název je příliš dlouhý."
    if re.match(r"^[a-zA-Z]:", stripped):
        return "Název nesmí být absolutní cesta."
    return None


def validate_generated_text(text: str) -> str | None:
    if text is None:
        return "Text je prázdný."
    return None


def sanitize_patterns(patterns: list[str]) -> list[str]:
    result = []
    for p in patterns:
        if p is not None:
            s = p.strip()
            if s != "":
                result.append(s)
    return result
