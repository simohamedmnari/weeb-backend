from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class AutoRefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()

        try:
            # Essaye d'authentifier normalement (token OK)
            auth.authenticate(request)
            return None

        except InvalidToken:
            # Token expiré → on tente un refresh via le cookie
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return None

            try:
                token = RefreshToken(refresh_token)
                new_access = str(token.access_token)

                # Injecte le nouveau token SimpleJWT dans la requête
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"

            except TokenError:
                return None

        return None
