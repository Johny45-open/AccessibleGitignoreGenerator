TEMPLATE_ENV = {
    "header": "Tajne soubory",
    "rules": [
        ".env",
    ],
}

TEMPLATE_ENV_STAR = {
    "header": "Tajne soubory",
    "rules": [
        ".env.*",
        "!.env.example",
    ],
}

TEMPLATE_CONFIG_LOCAL = {
    "header": "Tajne soubory",
    "rules": [
        "config.local.*",
        "*.local",
    ],
}
