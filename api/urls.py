from django.urls import path
from .views import (
    # AUTH
    login_view,

    # ARTICLES
    articles_list_create,
    article_detail,

    # ASSISTANT IA
    assistant_ia,
    improve_article,

    # CONTACT
    contact_message,
    list_contact_messages,

    # ANALYZE MESSAGE (NLP)
    analyze_message,

    # PREDICTIONS ML (ancienne logique)
    create_prediction,
    list_predictions_for_contact,

    # PREDICTION ML (vrai modèle predict.py)
    predict_message_api,



    # SENTRY DEBUG
    trigger_error,   # ← AJOUT ICI
)

urlpatterns = [
    # ============================================================
    # AUTH
    # ============================================================
    path("auth/login/", login_view, name="login"),

    # ============================================================
    # ARTICLES
    # ============================================================
    path("articles/", articles_list_create, name="articles-list-create"),
    path("articles/<int:pk>/", article_detail, name="article-detail"),

    # ============================================================
    # ASSISTANT IA
    # ============================================================
    path("assistant-ia/", assistant_ia, name="assistant-ia"),
    path("assistant-ia/improve/", improve_article, name="assistant-improve"),

    # ============================================================
    # CONTACT
    # ============================================================
    path("contact/", contact_message, name="contact-message"),
    path("contact/messages/", list_contact_messages, name="contact-messages"),

    # ============================================================
    # ANALYZE MESSAGE (NLP)
    # ============================================================
    path("contact/analyze/", analyze_message, name="analyze-message"),

    # ============================================================
    # PREDICTIONS ML (ancienne logique)
    # ============================================================
    path("contact/predictions/", create_prediction, name="create-prediction"),
    path("contact/<int:contact_id>/predictions/", list_predictions_for_contact, name="predictions-for-contact"),

    # ============================================================
    # PREDICTION ML (vrai modèle predict.py)
    # ============================================================
    path("predict/", predict_message_api, name="predict-message"),



        # ============================================================
    # SENTRY DEBUG
    # ============================================================
    path("sentry-debug/", trigger_error, name="sentry-debug"),
]

