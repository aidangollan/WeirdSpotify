from flask import Flask, request, jsonify, send_from_directory, redirect, session
from search import search_algo
from auth import get_token
from db import db
import requests
import os
from flask_cors import CORS
import base64
from create_playlist import create_playlist_on_spotify

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app, supports_credentials=True)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

# Spotify integration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

@app.route('/api/login')
def login():
    is_guest = request.args.get('guest') == 'true'
    
    if is_guest:
        session['user_type'] = 'guest'
        user_token = refresh_access_token(os.getenv('GUEST_REFRESH_TOKEN'))
        session['token'] = user_token
        return redirect("/search")

    session['user_type'] = 'normal'

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "scope": "playlist-modify-public",
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(os.getenv("AUTH_URL"), url_args)
    return redirect(auth_url)

def refresh_access_token(refresh_token):
    refresh_url = "https://accounts.spotify.com/api/token"
    headers = {
        'Authorization': f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    
    response = requests.post(refresh_url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print("Error in refreshing token:", response.content)
        return None


@app.route('/api/callback')
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": auth_token,
        "redirect_uri": os.getenv("REDIRECT_URI"),
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(os.getenv("TOKEN_URL"), data=code_payload)
    response_data = post_request.json()
    session['token'] = response_data["access_token"]

    return redirect("/search")

@app.route('/api/logout')
def logout():
    if session.get('user_type') == 'normal':
        session.pop('token', None)
    return redirect("/")

@app.route("/api/search", methods=["POST"])
def search():
    token = get_token()
    query = request.json.get("query").strip(" ")
    result = search_algo(token, query)
    
    return result

@app.route("/search")
def search_default():
    if session.get('user_type') is None:
        return redirect("/")
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/create_playlist", methods=["POST"])
def create_playlist():
    user_token = session.get('token')
    
    song_ids = request.json.get("song_ids")

    response_data = create_playlist_on_spotify(user_token, song_ids)

    if response_data["success"]:
        return jsonify(response_data)
    else:
        return jsonify(response_data), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()