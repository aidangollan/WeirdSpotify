from flask import Flask, request, jsonify, send_from_directory, redirect, session, url_for
from search import search_algo, search_for_song
from auth import get_token
from models import Song
from db import db
import requests
import os
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app, supports_credentials=True)
app.secret_key = 'some_secret'  # Change this to a proper secret key in production!
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

# Spotify integration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://sea-turtle-app-2-b6row.ondigitalocean.app/api/callback"
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/api/login')
def login():
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-modify-public",  # Only need permission to modify playlists
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(AUTH_URL, url_args)
    return redirect(auth_url)

@app.route('/api/callback')
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": auth_token,
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(TOKEN_URL, data=code_payload)
    response_data = post_request.json()
    print(response_data["access_token"])
    session['token'] = response_data["access_token"]
    print("session token")
    print(session['token'])
    
    return redirect(os.getenv("REACT_APP_URL"))

@app.route('/set_session')
def set_session():
    session['dummy'] = 'This is a test'
    return 'Session set'

@app.route('/get_session')
def get_session():
    return session.get('dummy', 'No session value')

@app.route('/api/logout')
def logout():
    session.pop('token', None)
    return redirect(os.getenv("REACT_APP_URL"))

@app.route("/api/search", methods=["POST"])
def search():
    print("in search")
    token = get_token() #my token, not user, used for searching for songs
    query = request.json.get("query").strip(" ")
    result = search_algo(token, query)
    
    if result:
        return jsonify(names=result)
    return jsonify(error="No songs found"), 404

@app.route("/search")
def search_default():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/create_playlist", methods=["POST"])
def create_playlist():
    print("in create playlist")
    user_token = session.get('token')
    dummy = session.get('dummy')
    if not user_token:
        print("user not logged in")
        print(user_token)
        return jsonify(error="User not logged in"), 401
    
    print(user_token)
    
    song_ids = request.json.get("song_ids")
    print(song_ids)
    print("song ids")
    # You'll need to implement the function below to create a playlist using the Spotify API
    success = create_playlist_on_spotify(user_token, song_ids)
    
    if success:
        return jsonify(success=True, message="Playlist created successfully")
    else:
        return jsonify(success=False, message="Failed to create playlist"), 500
    
def create_playlist_on_spotify(user_token, song_ids):
    print("in create playlist on spotify")
    print("song_ids")
    print(song_ids)
    SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
    HEADERS = {
        "Authorization": f"Bearer {user_token}"
    }

    # 1. Get the current user's ID
    current_user_request = requests.get(f"{SPOTIFY_API_BASE_URL}/me", headers=HEADERS)
    current_user_data = current_user_request.json()
    user_id = current_user_data['id']

    print(user_id)
    print("user id")

    # 2. Create a new playlist for the user
    create_playlist_data = {
        "name": "My Custom Playlist",
        "description": "Created using Weird Spotify",
        "public": True
    }
    create_playlist_request = requests.post(f"{SPOTIFY_API_BASE_URL}/users/{user_id}/playlists", headers=HEADERS, json=create_playlist_data)
    new_playlist_data = create_playlist_request.json()
    playlist_id = new_playlist_data['id']

    print(playlist_id)
    print("playlist id")

    # 3. Add tracks to the new playlist
    add_tracks_data = {
        "uris": [f"spotify:track:{song_id}" for song_id in song_ids]
    }
    add_tracks_request = requests.post(f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks", headers=HEADERS, json=add_tracks_data)
    add_tracks_response = add_tracks_request.json()

    print(add_tracks_response)
    print("add tracks response")

    print(add_tracks_request.status_code)
    print("add tracks request status code")

    if add_tracks_request.status_code == 201:  # 201 means tracks added successfully
        return True
    else:
        return False

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()