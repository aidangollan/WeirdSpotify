from flask import Flask, request, jsonify, send_from_directory
from search import search_algo, search_for_song
from auth import get_token
from models import Song
from db import db
import json
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

@app.route("/api/search", methods=["POST"])
def search():
    token = get_token()
    query = request.json.get("query").strip(" ")
    print(query)
    result = search_algo(token, query)
    
    if result:
        return jsonify(names=result)
    return jsonify(error="No songs found"), 404

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()