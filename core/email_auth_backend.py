from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Backend d'authentification basé sur l'email.
    Utilisé pour permettre la connexion avec CustomUser (USERNAME_FIELD = 'email').
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authentifie un utilisateur en utilisant son email et son mot de passe.
        """
        email = username or kwargs.get("email")
        if not email or not password:
            return None

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        # Vérifie le mot de passe + l'état du compte
        if user.check_password(password) and user.is_active:
            return user

        return None
