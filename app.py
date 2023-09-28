from flask import Flask, render_template as RenderTemplate, request
from oldCode import search_algo, search_for_song
from auth import get_token, get_auth_header

app = Flask(__name__)

@app.route("/")
def main():
    return RenderTemplate("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        token = get_token()
        names = []
        '''
        for word in open("google-10000-english.txt", "r"):
            word = word.strip()
            print(type(word))
            print(f"|{word}|")
            print(search_algo(token, word))
        '''
        query = request.form.get("query")
        result = search_algo(token, query)
        print(f"result is {result}")
        if result:
            return RenderTemplate("index.html", names = result)
        return RenderTemplate("index.html", names = ["Error: No songs found"])
        
    return RenderTemplate("index.html")


if __name__ == "__main__":
    app.run(debug=True)