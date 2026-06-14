from django.contrib import admin
from django.urls import path, include
from api.views import health_check

urlpatterns = [
    # ============================================================
    # ADMIN DJANGO
    # ============================================================
    path("admin/", admin.site.urls),

    # ============================================================
    # AUTHENTIFICATION (core)
    # ============================================================
    path("api/auth/", include("core.urls")),

    # ============================================================
    # API UNIFIÉE (articles + contact + prédictions ML)
    # ============================================================
    path("health/", health_check),
    path("api/", include("api.urls")),
]
