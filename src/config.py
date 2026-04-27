from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_OUTPUTS = PROJECT_ROOT / "data" / "outputs"

# Other directories
NOTEBOOKS = PROJECT_ROOT / "notebooks"
SRC = PROJECT_ROOT / "src"
MODELS = PROJECT_ROOT / "models"
REPORTS = PROJECT_ROOT / "reports"
REPORTS_CHARTS = REPORTS / "charts"
REPORTS_TABLES = REPORTS / "tables"
REPORTS_DOCS = REPORTS / "docs"
REPORTS_PRESENTATION = REPORTS / "presentation"
DASHBOARD = PROJECT_ROOT / "dashboard"
ARCHIVE = PROJECT_ROOT / "archive"