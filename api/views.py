from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Article, ContactMessage, SatisfactionPrediction
from .serializers import (
    ArticleSerializer,
    ContactMessageSerializer,
    SatisfactionPredictionSerializer,
)

from openai import OpenAI
from django.conf import settings

# Import du vrai modèle ML
from .predict import predict_message


def get_openai_client():
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return None, Response(
            {"error": "OPENAI_API_KEY manquante dans les settings Django."},
            status=500,
        )
    return OpenAI(api_key=api_key), None


# ============================================================
# AUTH — LOGIN (JWT)
# ============================================================

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email et mot de passe requis."}, status=400)

    from django.contrib.auth import authenticate
    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response({"error": "Identifiants invalides."}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "is_staff": user.is_staff,
            },
        },
        status=200
    )


# ============================================================
# ARTICLES (PROTÉGÉ)
# ============================================================

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def articles_list_create(request):
    user = request.user

    if request.method == "GET":
        articles = Article.objects.filter(user=user).order_by("-created_at")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=200)

    if request.method == "POST":
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            article = serializer.save(user=user)
            return Response(ArticleSerializer(article).data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def article_detail(request, pk):
    user = request.user

    try:
        article = Article.objects.get(pk=pk, user=user)
    except Article.DoesNotExist:
        return Response({"error": "Article introuvable."}, status=404)

    if request.method == "GET":
        return Response(ArticleSerializer(article).data, status=200)

    if request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        article.delete()
        return Response({"status": "deleted"}, status=204)


# ============================================================
# ASSISTANT IA — GENERATE ARTICLE (PUBLIC)
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def assistant_ia(request):

    topic = request.data.get("topic")
    audience = request.data.get("audience", "grand public")
    tone = request.data.get("tone", "neutre")
    length = request.data.get("length", "moyen")

    if not topic:
        return Response({"error": "Le champ 'topic' est obligatoire."}, status=400)

    prompt = (
        f"Crée un article complet sur le sujet : {topic}. "
        f"Public cible : {audience}. "
        f"Ton : {tone}. "
        f"Longueur : {length}. "
        "Génère un titre percutant, un plan structuré et un texte clair et professionnel."
    )

    client, error_response = get_openai_client()
    if error_response is not None:
        return error_response

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant IA expert en rédaction d’articles. "
                        "Tu génères un titre, un plan et un texte complet."
                    )
                },
                {"role": "user", "content": prompt},
            ],
        )

        answer = completion.choices[0].message.content
        return Response({"article": answer}, status=200)

    except Exception as e:
        print("Erreur OpenAI assistant_ia:", e)
        return Response({"error": "Erreur lors de l’appel à l’IA."}, status=500)


# ============================================================
# ASSISTANT IA — IMPROVE ARTICLE (PUBLIC)
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def improve_article(request):

    content = request.data.get("content")
    tone = request.data.get("tone", "neutre")
    audience = request.data.get("audience", "grand public")
    length = request.data.get("length", "moyen")

    if not content:
        return Response({"error": "Le champ 'content' est obligatoire."}, status=400)

    prompt = f"""
Tu es un assistant expert en rédaction.
Améliore le texte suivant en respectant ces règles :

- Garder le sens original
- Améliorer la clarté, la fluidité et la structure
- Adapter le ton : {tone}
- Adapter le public cible : {audience}
- Longueur souhaitée : {length}
- Corriger les fautes
- Reformuler si nécessaire
- Ne pas ajouter d’informations inventées

TEXTE À AMÉLIORER :
\"\"\"{content}\"\"\"
"""

    client, error_response = get_openai_client()
    if error_response is not None:
        return error_response

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant IA expert en amélioration de texte."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        improved = completion.choices[0].message.content
        return Response({"improved": improved}, status=200)

    except Exception as e:
        print("Erreur OpenAI improve_article:", e)
        return Response({"error": "Erreur lors de l’appel à l’IA."}, status=500)


# ============================================================
# CONTACT MESSAGE
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def contact_message(request):
    data = request.data.copy()

    if "consent" not in data or data["consent"] in ["false", False, "0", 0]:
        return Response({"error": "Le consentement RGPD est obligatoire."}, status=400)

    serializer = ContactMessageSerializer(data=data)

    if serializer.is_valid():
        msg = serializer.save()
        return Response(
            {
                "id": msg.id,
                "status": "received",
                "message": "Message reçu avec succès."
            },
            status=201
        )

    return Response(serializer.errors, status=400)


# ============================================================
# CONTACT LIST (PROTÉGÉ)
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def list_contact_messages(request):
    if not request.user.is_staff:
        return Response({"error": "Accès refusé."}, status=403)

    messages = ContactMessage.objects.all().order_by("-created_at")
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)


# ============================================================
# ANALYZE MESSAGE (NLP SIMPLE)
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def analyze_message(request):

    message = request.data.get("message", "").strip()

    if not message:
        return Response({"error": "Le champ 'message' est obligatoire."}, status=400)

    msg = message.lower()

    if "merci" in msg or "super" in msg or "parfait" in msg:
        theme = "positif"
        confidence = 0.95
    elif "problème" in msg or "mauvais" in msg or "nul" in msg:
        theme = "négatif"
        confidence = 0.85
    else:
        theme = "neutre"
        confidence = 0.60

    return Response({"theme": theme, "confidence": confidence}, status=200)


# ============================================================
# PREDICTIONS ML (CORRIGÉ)
# ============================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def create_prediction(request):

    contact_id = request.data.get("contact")
    text = request.data.get("text", "").strip()   # récupère le texte envoyé

    if not contact_id:
        return Response({"error": "Le champ 'contact' est obligatoire."}, status=400)

    if not text:
        return Response({"error": "Le champ 'text' est obligatoire."}, status=400)

    try:
        contact = ContactMessage.objects.get(pk=contact_id)
    except ContactMessage.DoesNotExist:
        return Response({"error": "Contact introuvable."}, status=404)

    # On utilise le texte envoyé par le frontend
    result = predict_message(text)

    prediction = result["prediction"]
    confidence = max(result["probabilities"].values()) if result["probabilities"] else None

    # 2. Sauvegarde en base
    pred = SatisfactionPrediction.objects.create(
        contact=contact,
        prediction=prediction,
        confidence=confidence
    )

    return Response(
        {
            "id": pred.id,
            "prediction": pred.prediction,
            "confidence": pred.confidence,
            "status": "prediction_saved"
        },
        status=201
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def list_predictions_for_contact(request, contact_id):
    if not request.user.is_staff:
        return Response({"error": "Accès refusé."}, status=403)

    try:
        contact = ContactMessage.objects.get(pk=contact_id)
    except ContactMessage.DoesNotExist:
        return Response({"error": "Message contact introuvable."}, status=404)

    predictions = contact.predictions.all().order_by("-created_at")
    serializer = SatisfactionPredictionSerializer(predictions, many=True)

    return Response(serializer.data, status=200)


# ============================================================
# PREDICTION ML — VRAI MODELE (predict.py)
# ============================================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .predict import predict_message

@api_view(["POST"])
@permission_classes([AllowAny])
def predict_message_api(request):
    text = request.data.get("message", "").strip()

    if not text:
        return Response({"error": "Le champ 'message' est obligatoire."}, status=400)

    result = predict_message(text)
    return Response(result, status=200)

# ============================================================
# HEALTH CHECK (PUBLIC)
# ============================================================

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})




def trigger_error(request):
    1 / 0

