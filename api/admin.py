from django.contrib import admin
from .models import ContactMessage, SatisfactionPrediction

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(SatisfactionPrediction)
class SatisfactionPredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "contact", "prediction", "confidence", "created_at")
    list_filter = ("prediction", "created_at")
    ordering = ("-created_at",)
