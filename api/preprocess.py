import re
import nltk
from nltk.corpus import stopwords

# Charger les stopwords anglais
stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """
    Nettoie un message utilisateur pour le préparer à la vectorisation.
    """
    text = text.lower()                               # minuscules
    text = re.sub(r"[^\w\s]", " ", text)              # retirer ponctuation
    text = re.sub(r"\d+", " ", text)                  # retirer chiffres
    text = " ".join([w for w in text.split() if w not in stop_words])  # retirer stopwords
    text = re.sub(r"\s+", " ", text).strip()          # nettoyer espaces multiples
    return text
