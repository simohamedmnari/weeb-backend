import os
from joblib import load
from .preprocess import clean_text   # ⬅ IMPORTANT : on utilise le vrai preprocess

# --- 1. Charger le modèle et le vectorizer ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

vectorizer = load(os.path.join(MODEL_DIR, "vectorizer.joblib"))
model = load(os.path.join(MODEL_DIR, "classifier.joblib"))

# --- 2. Fonction de prédiction ---
def predict_message(message: str):
    if not message:
        return {
            "message": "",
            "clean_message": "",
            "prediction": None,
            "probabilities": None
        }

    # Nettoyage IDENTIQUE au notebook
    clean = clean_text(message)

    # Vectorisation
    vect = vectorizer.transform([clean])

    # Prédiction
    prediction = model.predict(vect)[0]

    # Probabilités si dispo
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vect)[0]
        probabilities = {
            "insatisfaction": float(proba[0]),
            "satisfaction": float(proba[1])
        }
    else:
        probabilities = None

    return {
        "message": message,
        "clean_message": clean,
        "prediction": int(prediction),
        "probabilities": probabilities
    }
