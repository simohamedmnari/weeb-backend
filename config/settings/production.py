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

    # FRONTEND VERCEL 
    "weeb-frontend-v2.vercel.app",
    "weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================
# CORS — STRICT (PRODUCTION)
# ============================================================

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # FRONTEND VERCEL
    "https://weeb-frontend-v2.vercel.app",
    "https://weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

# IMPORTANT : autoriser les headers nécessaires
CORS_ALLOW_HEADERS = ["*"]
CORS_EXPOSE_HEADERS = ["*"]


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
# HTTPS — REDIRECTION & HSTS
# ============================================================

SECURE_SSL_REDIRECT = True  # force HTTPS

SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ============================================================
# OPENAI — Production
# ============================================================

OPENAI_API_KEY = config("OPENAI_API_KEY")
