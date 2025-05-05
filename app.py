from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["tp_scraping_dv"]
collection = db["articles"]

@app.route("/", methods=["GET"])
def index():
    auteur = request.args.get("auteur", "").strip()
    tag = request.args.get("tag", "").strip()
    date_min = request.args.get("date", "").strip()

    query = {}
    if auteur:
        query["author"] = {"$regex": auteur, "$options": "i"}
    if tag:
        query["tag"] = {"$regex": tag, "$options": "i"}
    if date_min:
        query["date"] = {"$gte": date_min}

    articles = list(collection.find(query).sort("date", -1))

    return render_template("index.html", articles=articles, auteur=auteur, tag=tag, date=date_min)

if __name__ == "__main__":
    app.run(debug=True)
