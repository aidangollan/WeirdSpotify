from flask import Flask, render_template as RenderTemplate, request
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
depth = "50"

@app.route("/")
def main():
    return RenderTemplate("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        token = get_token()
        names = []
        query = request.form.get("query")
        result = search_algo(token, query)
        print(f"result is {result}")
        if result:
            return RenderTemplate("index.html", names = result)
        return RenderTemplate("index.html", names = ["Error: No songs found"])
    return RenderTemplate("index.html")

def search_algo(token, query):
    '''
    print(f"query is {query}")
    words = query.split(" ")
    out = []
    matched_indices = set()  # To keep track of matched word indices

    # Start with the full length of the query and reduce the window size in each iteration
    for window_size in range(len(words), 0, -1):
        i = 0
        while i < len(words) - window_size + 1:
            # Skip if any word in the current window has been matched before
            if any(idx in matched_indices for idx in range(i, i+window_size)):
                i += 1
                continue

            substring = ' '.join(words[i:i+window_size])
            print(f"searching for substring {substring}")
            result = search_for_song(token, substring)
            print(f"the result is {result}")
            if result is None:
                i += 1
                continue
            matched = False
            for entry in result:
                song_name = entry["name"].lower()
                if substring.lower() == song_name:
                    print(f"found substring in song: {song_name}")
                    out.append(f"song: {entry['name']} by: {entry['artists'][0]['name']}")
                    # Mark the words in the matched substring
                    matched_indices.update(range(i, i+window_size))
                    matched = True
                    break
            if not matched:
                i += 1

    
    # Check if all words have been matched
    if len(matched_indices) != len(words):
        return ["Error: Not all words were matched"]
    
    return out
    '''
    out = []
    result = search_for_song(token, query)
    if result is not None:
        for r in result:
            out.append(r['name'])
        return out
    else:
        return ["No Song"]

def search_for_song(token, song_name, max_pages=1000):
    try:
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        base_query = f'?q=track:"{song_name}"&type=track&limit={depth}'

        page_count = 0
        exact_matches = []

        while page_count < max_pages:
            offset = page_count * int(depth)
            query_url = f"{url}{base_query}&offset={offset}"

            result = get(query_url, headers=headers)
            if not result:
                print(f"no result on page {offset}")
                break
            try:
                json_content = json.loads(result.content)
                json_result = json_content["tracks"]["items"]
                if len(json_result) == 0:
                    print("no songs by that name")
                    break
                for s in json_result:
                    print(s['name'])
                # Filter the results to only include exact matches
                exact_matches.extend([song for song in json_result if song["name"].lower() == song_name.lower()])

                # If an exact match is found, break out of the loop
                if exact_matches:
                    break

                page_count += 1
            except:
                print()
                break
            print("|||||||||||")

        return exact_matches if exact_matches else None

    except Exception as e:
        print(f"the exception {e} occured")
        print("||||||||||||||||||||")
        print(f"the json file was {result}")
        print("||||||||||||||||||||")
        print(f"the song name was {song_name}")


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",\
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


if __name__ == "__main__":
    app.run(debug=True)