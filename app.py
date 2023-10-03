from flask import Flask, render_template as RenderTemplate, request
from search import search_algo, search_for_song
from auth import get_token
from models import Song
from db import db
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

@app.route("/")
def main():
    return RenderTemplate("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        token = get_token()
        query = request.form.get("query")
        result = search_algo(token, query)
        if result:
            return RenderTemplate("index.html", names = result)
        return RenderTemplate("index.html", names = ["Error: No songs found"])
        
    return RenderTemplate("index.html")

@app.route("/add_to_db", methods=["GET", "POST"])
def add_to_db():
    if request.method == "POST":
        token = get_token()
        for word in open("google-10000-english.txt", "r"):
            word = word.strip()
            result = search_for_song(token, word)
            
            if result:
                # Add the song to the database
                song = Song(name=word, song_data=json.dumps(result))
                db.session.add(song)
                db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)