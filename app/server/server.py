from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import yaml
import json
import requests
import sqlite3

app = Flask(__name__)
CORS(app)
api = Api(app)

config = yaml.safe_load(open('config.yml'))
youtube_api_key = config['youtube_api_key']

@app.route('/tracks')
def get_tracks():
    cur = sqlite3.connect("songs.db").cursor()
    query = cur.execute("SELECT artist, name, year FROM songs")

    res = [{'artist': t[0], 'name': t[1], 'year': t[2]} for t in query.fetchall()]
    return res

@app.route('/search_video')
def search_video():
    query = request.args.get('query')
    url = f"https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&type=video&part=snippet&q={query}"
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)

    id = data["items"][0]["id"]["videoId"]
    print(id)
    return id


if __name__ == '__main__':
    app.run(debug=True)
