from .base import *
import dj_database_url
from decouple import config
from pathlib import Path

# ============================================================
# SÉCURITÉ (PRODUCTION)
# ============================================================

SECRET_KEY = config("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = [
    config("RAILWAY_PUBLIC_DOMAIN", default=""),
    config("ALLOWED_HOSTS", default="").replace(" ", ""),
]

# ============================================================
# BASE DE DONNÉES — POSTGRESQL (Railway)
# ============================================================

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# ============================================================
# STATIC FILES — WhiteNoise
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# CORS — STRICT (PRODUCTION)
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    config("FRONTEND_URL", default=""),
]

CORS_ALLOW_CREDENTIALS = True

# ============================================================
# COOKIES — SÉCURISÉS (HTTPS)
# ============================================================

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

SIMPLE_JWT["AUTH_COOKIE_SECURE"] = True
SIMPLE_JWT["AUTH_COOKIE_SAMESITE"] = "None"

# ============================================================
# OPENAI — Production
# ============================================================

OPENAI_API_KEY = config("OPENAI_API_KEY")
