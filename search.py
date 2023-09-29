from auth import get_auth_header
from requests import get
import json
depth = "50"


def search_algo(token, query):
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
            #print(f"searching for substring {substring}")
            result = search_for_song(token, substring)
            #print(f"the result is {result}")
            if result is None:
                i += 1
                continue
            matched = False
            for entry in result:
                song_name = entry["name"].lower()
                if substring.lower() == song_name:
                    #print(f"found substring in song: {song_name}")
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
    
def search_for_song(token, song_name, max_pages=100):
    try:
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
                #print(f"no result on page {offset}")
                break
            try:
                json_content = json.loads(result.content)
                json_result = json_content["tracks"]["items"]
                #for song in json_result:
                    #print(song["name"])
                if len(json_result) == 0:
                    #print("no songs by that name")
                    break
                #for s in json_result:
                    #print(s['name'])
                # Filter the results to only include exact matches
                exact_matches.extend([song for song in json_result if song["name"].lower() == song_name.lower()])

                # If an exact match is found, break out of the loop
                if exact_matches:
                    break

                page_count += 1
            except:
                #print()
                break

        return exact_matches if exact_matches else None

    except Exception as e:
        print(f"the exception {e} occured")
        print("||||||||||||||||||||")
        print(f"the json file was {result}")
        print("||||||||||||||||||||")
        print(f"the song name was {song_name}")