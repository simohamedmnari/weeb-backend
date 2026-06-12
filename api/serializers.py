from rest_framework import serializers
from .models import Article, ContactMessage, SatisfactionPrediction

# ============================================================
# ARTICLE
# ============================================================

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "user",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


# ============================================================
# CONTACT MESSAGE
# ============================================================

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "email",
            "message",
            "consent",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# ============================================================
# SATISFACTION PREDICTION
# ============================================================

class SatisfactionPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatisfactionPrediction
        fields = [
            "id",
            "contact",
            "prediction",
            "confidence",
            "created_at",
        ]
        # Correction essentielle :
        # prediction + confidence doivent être calculés par le backend (modèle ML)
        read_only_fields = ["id", "created_at", "prediction", "confidence"]
