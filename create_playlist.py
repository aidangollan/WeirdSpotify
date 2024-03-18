import time
import requests

def create_playlist_on_spotify(user_token, song_ids):
    try:
        SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
        HEADERS = {
            "Authorization": f"Bearer {user_token}"
        }

        current_user_request = requests.get(f"{SPOTIFY_API_BASE_URL}/me", headers=HEADERS)
        current_user_data = current_user_request.json()
        user_id = current_user_data['id']

        create_playlist_data = {
            "name": "My Custom Playlist",
            "description": "Created using weirdspotify.com",
            "public": True
        }
        create_playlist_request = requests.post(f"{SPOTIFY_API_BASE_URL}/users/{user_id}/playlists", headers=HEADERS, json=create_playlist_data)
        new_playlist_data = create_playlist_request.json()
        playlist_id = new_playlist_data['id']


        add_tracks_data = {
            "uris": [f"spotify:track:{song_id}" for song_id in song_ids]
        }
        add_tracks_request = requests.post(f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks", headers=HEADERS, json=add_tracks_data)
        add_tracks_response = add_tracks_request.json()

        time.sleep(.5)

        if add_tracks_request.status_code < 300:
            return {
                "success": True,
                "message": "Playlist created successfully",
                "playlist_url": new_playlist_data['external_urls']['spotify']
            }
        else:
            return {
                "success": False,
                "message": "Failed to add tracks to the playlist",
                "playlist_url": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "playlist_url": None
        }