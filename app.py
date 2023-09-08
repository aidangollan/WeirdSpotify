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

@app.route("/")
def main():
    return RenderTemplate("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        token = get_token()
        names = []
        name = request.form.get("query")
        result = search_for_song(token, name)
        for i in range(len(result)):
            names.append(result[i]["name"])
        return RenderTemplate("index.html", names = names)
    return RenderTemplate("index.html")

def search_for_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=10"

    query_url = url + query

    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("no songs by that name")
        return None
    return json_result

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