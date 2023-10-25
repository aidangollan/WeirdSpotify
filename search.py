from auth import get_auth_header, get_token
from requests import get
import json
import os
from models import Song
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

#from dotenv import load_dotenv
#load_dotenv()

depth = "50"
DATABASE_URI = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def search_algo(token, query):
    words = [word for word in query.split() if word]
    out = []
    matched_indices = set()  # To keep track of matched word indices
    unmatched_words = set(words)  # New set to store unmatched words

    for window_size in range(1, len(words) + 1):
        for i in range(len(words) - window_size + 1):
            # If the current word is already matched, skip
            if any(idx in matched_indices for idx in range(i, i + window_size)):
                continue

            substring = ' '.join(words[i:i + window_size])
            
            # First, check in the database
            db_result = search_in_database(substring)
            if db_result:
                out.append(db_result)
                matched_indices.update(range(i, i + window_size))
                unmatched_words.difference_update(words[i:i + window_size])
                continue 

            # If not found in the database, then check Spotify
            results = search_for_song(token, substring)
            if results:
                for entry in results:
                    song_name = entry["name"].lower()
                    if substring.lower() == song_name:
                        song_data = {
                            'id': entry['id'],
                            'name': entry['name'],
                            'artist': entry['artists'][0]['name'],
                            'image_url': entry['album']['images'][0]['url'] if entry['album']['images'] else None
                        }
                        out.append(song_data)
                        matched_indices.update(range(i, i + window_size))
                        unmatched_words.difference_update(words[i:i + window_size])
                        break

    # Check if there are unmatched words and provide error messages for each one
    error_messages = [f"Error: word '{word}' is not a Spotify Song" for word in unmatched_words]

    print(f"out: {out}")
    print(f"errors: {error_messages}")
    return {'songs': out, 'errors': error_messages}

def search_in_database(song_name):
    """Search the song in the database"""
    session = Session()

    # Query the database for the song
    song = session.query(Song).filter_by(name = song_name).first()

    session.close()

    if song:
        # Deserialize the song_data string into a Python dictionary
        song_data = json.loads(song.song_data)
        songs_len = len(song_data)
        song_idx = random.randint(0, songs_len - 1)
        
        # Return the formatted data
        return {
            'id': song_data[song_idx]['id'],
            'name': song.name,
            'artist': song_data[song_idx]['artists'][0]['name'],
            'image_url': song_data[song_idx]['album']['images'][0]['url'] if song_data[song_idx]['album']['images'] else None
        }
    return None
    
def search_for_song(token, song_name, max_pages=5):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    base_query = f'?q={song_name}&type=track&market=US&limit={depth}'

    page_count = 0
    exact_matches = []

    while page_count < max_pages:
        offset = page_count * int(depth)
        query_url = f"{url}{base_query}&offset={offset}"

        result = get(query_url, headers=headers)
        if not result:
            break
        try:
            json_content = json.loads(result.content)
            json_result = json_content["tracks"]["items"]
            if len(json_result) == 0:
                break
            exact_matches.extend([song for song in json_result if song["name"].lower() == song_name.lower()])

            # If an exact match is found, break out of the loop
            if exact_matches:
                break

            page_count += 1
        except:
            break

    return exact_matches if exact_matches else None