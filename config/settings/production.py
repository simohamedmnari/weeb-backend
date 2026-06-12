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
    "weeb-backend-production.up.railway.app",
    "localhost",
    "127.0.0.1",
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

# WhiteNoise doit être juste après SecurityMiddleware
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# CORS — STRICT (PRODUCTION)
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # NOUVEAUX DOMAINES VERCEL (OBLIGATOIRES)
    "https://weeb-frontend-v2.vercel.app",
    "https://weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

# ============================================================
# CSRF — TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    "https://weeb-backend-production.up.railway.app",

    # NOUVEAUX DOMAINES VERCEL (OBLIGATOIRES)
    "https://weeb-frontend-v2.vercel.app",
    "https://weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

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
