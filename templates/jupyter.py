TEMPLATE = {
    "header": "Jupyter Notebook",
    "rules": [
        ".ipynb_checkpoints/",
        "*.ipynb",
        # Note: we do NOT ignore *.ipynb by default for Python+Jupyter,
        # but we add checkpoints. User can extend.
    ],
}

# For cleaner generation we keep checkpoints only, notebooks themselves are source.
# Re-evaluate: don't ignore *.ipynb, only checkpoints
JUPYTER_RULES = [
    ".ipynb_checkpoints/",
]

DATASET_RULES = {
    "header": "Data a datasety",
    "rules": [
        "data/",
        "dataset/",
        "*.csv",
        "*.parquet",
    ],
}

TEMP_RULES = {
    "header": "Docasne soubory",
    "rules": [
        "*.tmp",
        "*.temp",
        "*.swp",
        "*~",
    ],
}

CACHE_RULES = {
    "header": "Cache",
    "rules": [
        ".cache/",
        ".mypy_cache/",
        ".ruff_cache/",
    ],
}

LOGS_RULES = {
    "header": "Logy",
    "rules": [
        "*.log",
        "logs/",
    ],
}
