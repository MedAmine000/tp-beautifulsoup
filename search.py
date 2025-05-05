from pymongo import MongoClient
from datetime import datetime

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tp_scraping"]
collection = db["articles"]

def afficher_resultats(resultats):
    for i, article in enumerate(resultats, 1):
        print(f"\nArticle {i}:")
        print(f"  Titre     : {article.get('title')}")
        print(f"  Auteur    : {article.get('author')}")
        print(f"  Tag       : {article.get('tag')}")
        print(f"  Date      : {article.get('date')}")
        print(f"  Résumé    : {article.get('summary')}")
        print(f"  URL       : {article.get('url')}")

def rechercher_articles():
    print("=== Recherche d'articles ===")
    auteur = input("Filtrer par auteur (laisser vide si aucun) : ").strip()
    tag = input("Filtrer par tag (laisser vide si aucun) : ").strip()
    date_min = input("Filtrer après date (AAAA-MM-JJ, laisser vide si aucun) : ").strip()

    query = {}

    if auteur:
        query["author"] = {"$regex": auteur, "$options": "i"}  # insensible à la casse
    if tag:
        query["tag"] = {"$regex": tag, "$options": "i"}
    if date_min:
        try:
            datetime.strptime(date_min, "%Y-%m-%d")  # vérif format
            query["date"] = {"$gte": date_min}
        except:
            print("⚠️ Format de date incorrect. Ignoré.")

    resultats = list(collection.find(query).sort("date", -1))

    print(f"\n🔎 {len(resultats)} article(s) trouvé(s)")
    afficher_resultats(resultats)

if __name__ == "__main__":
    rechercher_articles()
