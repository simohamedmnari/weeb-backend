from django.contrib import admin
from django.urls import path, include

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
    path("api/", include("api.urls")),
]
