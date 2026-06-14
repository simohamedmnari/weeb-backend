from .base import *
import dj_database_url
from decouple import config
from pathlib import Path

SECRET_KEY = config("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = [
    "weeb-backend-production.up.railway.app",
    "localhost",
    "127.0.0.1",
    "weeb-frontend-v2.vercel.app",
    "weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://weeb-frontend-v2.vercel.app",
    "https://weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "dnt",
    "connection",
    "pragma",
    "cache-control",
    "x-csrftoken",
]

CORS_EXPOSE_HEADERS = [
    "Content-Type",
    "X-CSRFToken",
    "Set-Cookie",
]

CSRF_TRUSTED_ORIGINS = [
    "https://weeb-backend-production.up.railway.app",
    "https://weeb-frontend-v2.vercel.app",
    "https://weeb-frontend-v2-iomihp3tx-mnpinvests-projects.vercel.app",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

OPENAI_API_KEY = config("OPENAI_API_KEY")
