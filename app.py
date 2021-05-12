from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scrape import scrape_all

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_app")

@app.route("/")
def index():
    collection = mongo.db.page_data.find_one()
    return render_template("index.html", collection=collection)


@app.route("/scrape")
def scrape():
    collection = mongo.db.page_data
    page_data = scrape_all()
    collection.update({}, page_data, upsert=True)
    return "Scraping successful!"


if __name__ == "__main__":
    app.run()
