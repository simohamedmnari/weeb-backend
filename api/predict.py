import os
import pandas as pd
from joblib import load
from preprocess import clean_text

# --- 1. Charger le modèle et le vectorizer ---
MODEL_DIR = os.path.join("..", "models")

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
        "prediction": prediction,
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
