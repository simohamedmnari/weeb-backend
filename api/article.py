# article.py
"""
Logique métier pour les Articles.
Ce fichier ne contient PAS de modèles Django.
Il sert uniquement à organiser la logique métier.
"""

def format_article_title(title: str) -> str:
    """
    Exemple de logique métier :
    - Nettoyage du titre
    - Mise en forme
    """
    return title.strip().capitalize()


def summarize_content(content: str) -> str:
    """
    Exemple de logique métier :
    - Générer un résumé simple
    - Utilisé éventuellement par l'assistant IA
    """
    if len(content) <= 200:
        return content
    return content[:200] + "..."
