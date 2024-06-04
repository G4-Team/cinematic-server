from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

URLS_DIR = BASE_DIR / "urls"
VIEW_DIR = BASE_DIR / "views"
MODELS_DIR = BASE_DIR / "models"
