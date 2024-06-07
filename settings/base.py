import urllib
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

URLS_DIR = BASE_DIR / "urls"


APPS = [
    "users",
]


DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DATABASE_CONNECT_STR = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@localhost:3306/cinematic"
)

JWT_SECRET = "TOP_SECRET_DONT_SEE"
