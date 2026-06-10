from django.db import models
from django.conf import settings

# ============================================================
# ARTICLE
# ============================================================

class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ============================================================
# CONTACT MESSAGE
# ============================================================

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ============================================================
# SATISFACTION PREDICTION
# ============================================================

class SatisfactionPrediction(models.Model):
    contact = models.ForeignKey(
        ContactMessage,
        on_delete=models.CASCADE,
        related_name="predictions"
    )
    prediction = models.IntegerField()  # 0 = pas satisfait, 1 = satisfait
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.prediction} (Contact {self.contact.id})"
