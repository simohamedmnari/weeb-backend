from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    LogoutView,
    MeView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from .token import CustomTokenObtainPairView


urlpatterns = [
    # AUTH CLASSIQUE (tes endpoints actuels)
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),

    # 🔥 NOUVEAU : TOKEN JWT AVEC is_staff, is_superuser, email, user_type
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
