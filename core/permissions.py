from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Permission stricte :
    - l'objet doit avoir un attribut `user`
    - seul le propriétaire peut y accéder
    """

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "user") and obj.user == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Pour les Articles :
    - lecture ouverte (GET, HEAD, OPTIONS)
    - écriture/modification/suppression réservée au propriétaire
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(obj, "user") and obj.user == request.user
