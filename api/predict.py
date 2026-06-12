import os
import re
from joblib import load

# --- 0. Fonction clean_text intégrée (plus besoin de preprocess.py) ---
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- 1. Charger le modèle et le vectorizer ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = load(os.path.join(MODEL_DIR, "classifier.joblib"))
vectorizer = load(os.path.join(MODEL_DIR, "vectorizer.joblib"))

# --- 2. Fonction de prédiction ---
def predict_message(message: str):
    clean = clean_text(message)
    vect = vectorizer.transform([clean])
    prediction = model.predict(vect)[0]
    proba = model.predict_proba(vect)[0]

    return {
        "message": message,
        "clean_message": clean,
        "prediction": int(prediction),
        "probabilities": {
            "insatisfaction": float(proba[0]),
            "satisfaction": float(proba[1])
        }
    }

# --- 3. Test manuel ---
if __name__ == "__main__":
    msg = input("Entrez un message à analyser : ")
    result = predict_message(msg)

    print("\n=== Résultat ===")
    print(f"Texte nettoyé : {result['clean_message']}")
    print(f"Prédiction : {result['prediction']}")
    print("Probabilités :", result["probabilities"])
