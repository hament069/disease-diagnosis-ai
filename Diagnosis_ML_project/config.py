# import libraries
import os

# =====================================
# BASE ROOT
# =====================================

BASE_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

print(BASE_ROOT)

# =====================================
# FOLDERS
# =====================================

DATASETS = os.path.join(
    BASE_ROOT,
    "Datasets"
)

MODELS_PIPELINES = os.path.join(
    BASE_ROOT,
    "Models_Pipelines"
)

SCRIPTS = os.path.join(
    BASE_ROOT,
    "Scripts"
)

FRONTEND = os.path.join(
    SCRIPTS,
    "Frontend"
)

BACKEND = os.path.join(
    SCRIPTS,
    "Backend"
)

NOTEBOOKS = os.path.join(
    SCRIPTS,
    "Notebooks"
)

UTILS = os.path.join(
    SCRIPTS,
    "Utils"
)

TESTS = os.path.join(
    BASE_ROOT,
    "Tests"
)

# =====================================
# CREATE FOLDERS
# =====================================

folders = [
    DATASETS,
    MODELS_PIPELINES,
    SCRIPTS,
    FRONTEND,
    BACKEND,
    NOTEBOOKS,
    UTILS,
    TESTS
]

for folder in folders:
    os.makedirs(
        folder,
        exist_ok=True
    )

print(
    "Project structure created successfully."
)