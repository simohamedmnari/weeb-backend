import re

def clean_text(text: str) -> str:
    """
    Nettoie un message utilisateur pour le préparer à la vectorisation.
    """
    # Minuscule
    text = text.lower()

    # Retirer tout sauf lettres et espaces
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", " ", text)

    # Retirer les espaces multiples
    text = re.sub(r"\s+", " ", text).strip()

    return text
