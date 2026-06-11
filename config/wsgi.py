"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# ============================================================
# SETTINGS MODULE (PRODUCTION)
# ============================================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.production"
)

# ============================================================
# APPLICATION WSGI + WHITENOISE
# ============================================================

application = get_wsgi_application()

# WhiteNoise doit envelopper l'application WSGI
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(os.path.dirname(__file__)), "staticfiles")
)
