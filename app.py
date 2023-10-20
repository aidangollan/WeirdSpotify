from flask import Flask, request, jsonify, send_from_directory, redirect, session, url_for
from search import search_algo, search_for_song
from auth import get_token
from models import Song
from db import db
import requests
import os
from flask_cors import CORS
import base64

#from dotenv import load_dotenv
#load_dotenv()


app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app, supports_credentials=True)
app.secret_key = 'some_secret'  # Change this to a proper secret key in production!
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

# Spotify integration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

@app.route('/api/login')
def login():
    is_guest = request.args.get('guest') == 'true'
    
    if is_guest:
        # Handle the guest login logic here, for example:
        # Set the session['user_type'] = 'guest'
        session['user_type'] = 'guest'
        user_token = refresh_access_token(os.getenv('GUEST_REFRESH_TOKEN'))
        session['token'] = user_token
        return redirect("/search")

    
    # If not a guest, proceed with Spotify login
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
    
    print("Access Token:", session['token'])
    
    return redirect("/search")

@app.route('/api/logout')
def logout():
    if session.get('user_type') == 'normal':
        session.pop('token', None)
    return redirect("/")

@app.route("/api/search", methods=["POST"])
def search():
    print("in search")
    token = get_token() #my token, not user, used for searching for songs
    query = request.json.get("query").strip(" ")
    print(query)
    result = search_algo(token, query)
    print(result)
    
    return result

@app.route("/search")
def search_default():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/create_playlist", methods=["POST"])
def create_playlist():
    print("in create playlist")
    user_token = session.get('token')

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