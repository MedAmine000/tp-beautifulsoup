# TP - Web Scraping avec BeautifulSoup, MongoDB et Flask

Ce projet est un TP de scraping réalisé avec **BeautifulSoup4** pour extraire automatiquement les articles de la section "Web" du [Blog du Modérateur](https://www.blogdumoderateur.com/web/).

Les données sont enrichies (images, auteur, résumé, etc.) et stockées dans une base **MongoDB**. Le projet inclut aussi :
- Une **interface de recherche** web en Flask
- Un **script de recherche terminale** (`search.py`)

---

## 📂 Structure du projet

```
.
├── main.py          # Scraping complet avec pagination
├── search.py        # Recherche des articles dans MongoDB depuis le terminal
├── app.py           # Interface web Flask
├── templates/
│   └── index.html   # Affichage HTML des résultats
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/MedAmine000/tp-beautifulsoup.git
cd tp-beautifulsoup
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer le scraping

```bash
python main.py
```

> ✅ Les articles sont insérés ou mis à jour automatiquement (pas de doublons)

---

## 🌐 Interface web avec Flask

### Lancement

```bash
python app.py
```

Accès : [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Fonctions disponibles

- Recherche par **auteur**, **tag** ou **date minimale**
- Affichage :
  - Image principale
  - Titre cliquable
  - Résumé
  - Date, catégorie, auteur

---

## 🧪 Script de recherche terminal : `search.py`

```bash
python search.py
```

Permet d'effectuer une recherche d'articles depuis la console, par :
- Auteur (`--auteur`)
- Tag (`--tag`)
- Date minimale (`--date`)

Exemple :

```bash
python search.py --tag IA --date 2025-04-01
```

---

## 🗃️ MongoDB

La base de données locale utilisée est `tp_scraping_dv`, collection `articles`.

Un index unique est créé sur l'URL pour éviter les doublons :

```python
collection.create_index("url", unique=True)
```

Les données de chaque article incluent :

- `url`, `title`, `summary`
- `image` (miniature)
- `images` (toutes les images avec légende)
- `tag`, `date`, `author`

---

## 📦 Fichier `requirements.txt`

```
beautifulsoup4
requests
pymongo
flask
```

---

## 🧑‍💻 Auteur

Projet réalisé par **[Korniti / MedAmine]**  
Master M1 – IPSSI – TP Web Scraping

---

## 📝 Licence

Usage strictement académique.  
Les données scrappées restent la propriété du site Blog du Modérateur.
