# contact_prediction.py
"""
Logique métier pour :
- les messages Contact
- les prédictions ML de satisfaction

Ce fichier ne contient PAS de modèles Django.
Il sert uniquement à organiser la logique métier.
"""

def clean_contact_message(message: str) -> str:
    """
    Nettoyage simple du message :
    - suppression espaces inutiles
    - normalisation
    """
    return message.strip()


def analyze_sentiment_basic(message: str) -> int:
    """
    Exemple de logique métier simple :
    - Retourne 1 si message semble positif
    - Retourne 0 si message semble négatif
    (placeholder avant modèle ML réel)
    """
    positive_keywords = ["merci", "super", "bien", "satisfait", "parfait"]
    negative_keywords = ["problème", "mauvais", "insatisfait", "bug", "erreur"]

    msg = message.lower()

    if any(word in msg for word in positive_keywords):
        return 1
    if any(word in msg for word in negative_keywords):
        return 0

    return 1  # par défaut : positif


def compute_confidence(score: int) -> float:
    """
    Exemple de logique métier :
    - Convertit un score en confiance simple
    """
    return 0.90 if score == 1 else 0.75
