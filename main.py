import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tp_scraping_dv"]
collection = db["articles"]

collection.create_index("url", unique=True)

def format_date(raw_date):
    mois_fr = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    try:
        jour, mois, annee = raw_date.lower().split()
        mois = mois_fr[mois]
        jour = jour.zfill(2)
        return f"{annee}-{mois}-{jour}"
    except:
        return raw_date
def get_article_images(article_url):
    images = []
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for img in soup.find_all('img'):
            url = img.get('data-lazy-src') or img.get('src')
            caption = img.get('alt') or img.get('title') or ''
            if url:
                images.append({'url': url, 'caption': caption})
    except Exception as e:
        print(f"Erreur récupération images : {e}")
    return images

def get_author(article_url):
    try:
        response = requests.get(article_url)
        soup_article = BeautifulSoup(response.text, 'html.parser')
        author_link = soup_article.find('a', href=lambda href: href and '/auteur/' in href)
        return author_link.get_text(strip=True) if author_link else None
    except Exception as e:
        print(f"Erreur récupération auteur : {e}")
        return None

def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_tag = soup.find('main')
        if not main_tag:
            print("No <main> tag found.")
            return []

        articles = main_tag.find_all('article')
        print(f"Nombre d'articles trouvés : {len(articles)}")
        articles_data = []

        for article in articles:
            img_div = article.find('div', class_='post-thumbnail picture rounded-img')
            img_tag = img_div.find('img') if img_div else None
            img_url = img_tag.get('data-lazy-src') if img_tag else None

            meta_div = article.find('div', class_='entry-meta ms-md-5 pt-md-0 pt-3')
            tag = meta_div.find('span', class_='favtag color-b').get_text(strip=True) if meta_div else None
            date_raw = meta_div.find('span', class_='posted-on t-def px-3').get_text(strip=True) if meta_div else None
            date = format_date(date_raw) if date_raw else None

            header = meta_div.find('header', class_='entry-header pt-1') if meta_div else None
            a_tag = header.find('a') if header else None
            article_url = a_tag.get('href') if a_tag else None
            title = a_tag.find('h3').get_text(strip=True) if a_tag and a_tag.find('h3') else None

            summary_div = meta_div.find('div', class_='entry-excerpt t-def t-size-def pt-1') if meta_div else None
            summary = summary_div.get_text(strip=True) if summary_div else None

            author = get_author(article_url) if article_url else None
            images_list = get_article_images(article_url) if article_url else []

            if not article_url:
                continue  # skip invalid

            articles_data.append({
                'image': img_url,
                'tag': tag,
                'date': date,
                'url': article_url,
                'title': title,
                'summary': summary,
                'author': author,
                'images': images_list

            })

        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

def fetch_all_articles(base_url, max_pages):
    all_articles = []
    for page in range(1, max_pages + 1):
        print(f"🔄 Scraping page {page}")
        url = f"{base_url}/page/{page}/" if page > 1 else base_url
        articles = fetch_articles(url)
        if not articles:
            break
        all_articles.extend(articles)
    return all_articles

# Point d'entrée
base_url = "https://www.blogdumoderateur.com/web"
articles = fetch_all_articles(base_url, max_pages=20)

if articles:
    for article in articles:
        collection.update_one(
             {"url": article["url"]},  # critère d'unicité
             {"$set": article},        # mise à jour ou insertion
            upsert=True               # si non trouvé, on insère
        )


# Affichage simple
for i, article in enumerate(articles, 1):
    print(f"\nArticle {i}:")
    for k, v in article.items():
        print(f"{k.capitalize()}: {v}")
