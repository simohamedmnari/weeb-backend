# ============================================================
# IMPORTS GLOBAUX
# ============================================================

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser


# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"access": str(access)}, status=201)

        # Cookie refresh token
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24 * 30,
            path="/",
        )

        return response


# ============================================================
# LOGIN
# ============================================================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"access": str(access)}, status=200)

        # Cookie refresh token
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24 * 30,
            path="/",
        )

        return response


# ============================================================
# REFRESH TOKEN
# ============================================================

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token manquant."}, status=400)

        try:
            old_refresh = RefreshToken(refresh_token)

            user_id = old_refresh["user_id"]
            user = CustomUser.objects.get(id=user_id)

            new_refresh = RefreshToken.for_user(user)
            new_access = str(new_refresh.access_token)

            old_refresh.blacklist()

            response = Response({"access": new_access}, status=200)

            response.set_cookie(
                key="refresh_token",
                value=str(new_refresh),
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 30,
                path="/",
            )

            return response

        except Exception:
            return Response({"detail": "Refresh token invalide."}, status=401)


# ============================================================
# LOGOUT
# ============================================================

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response({"detail": "Déconnexion réussie."})
        response.delete_cookie("refresh_token", path="/")
        return response


# ============================================================
# ME — Infos utilisateur connecté
# ============================================================

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: CustomUser = request.user

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at,
            },
            status=200,
        )
