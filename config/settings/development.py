from .base import *
from decouple import config
from pathlib import Path

# ============================================================
# SÉCURITÉ (LOCAL)
# ============================================================

SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ============================================================
# BASE DE DONNÉES (LOCAL — SQLITE)
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ============================================================
# CORS (LOCAL)
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# ============================================================
# COOKIES (LOCAL)
# ============================================================

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# ============================================================
# SIMPLE JWT (LOCAL)
# ============================================================

SIMPLE_JWT["AUTH_COOKIE_SECURE"] = False

# ============================================================
# OPENAI (LOCAL)
# ============================================================

OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
