from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import yaml
import json
import requests
import sqlite3
import time
import re

app = Flask(__name__)
CORS(app)
api = Api(app)

config = yaml.safe_load(open('config.yml'))
youtube_api_key = config['youtube_api_key']
music_brainz_user_agent = "diskothekmann/0.0 ( thomas.staud05@gmail.com )"

# used to avoid calling music brainz api more than once per second
last_api_call = 0

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

'''
takes a youtube video id and returns a track (with artist, name and year)
this is done in two steps
1. retrieve video title from youtube API
2. try to extract song title
3. find corresponding song via MusicBrainz API (alternatively last.fm?)
'''
@app.route('/track_from_id')
def track_from_id():
    # throttle
    global last_api_call
    current_time = int(time.time())
    if last_api_call == current_time:
        print("throttled query (track_from_id)")
        return {'error': 'hey, stop spamming queries!'}
    last_api_call = current_time
    print(last_api_call)

    id = request.args.get('id')

    # 1. get video title
    url = f"https://www.googleapis.com/youtube/v3/videos?key={youtube_api_key}&part=snippet&id={id}"
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)

    # 2. extract title
    title = data["items"][0]["snippet"]["title"]
    # TODO: remove extras like '(20xx Remaster)' or 'Live at xxx'
    # in most cases filtering out artist name should be possible as well - but that's NOT the case for release year!!
    artist = data["items"][0]["snippet"]["channelTitle"][:-8]

    # 3. find track info
    sanitized_title = title.replace("&", "and")
    sanitized_artist = artist.replace("&", "and")
    url = f"http://musicbrainz.org/ws/2/recording/?query=recording:{sanitized_title}%20AND%20artist:{sanitized_artist}&fmt=json"
    headers = {'User-Agent': music_brainz_user_agent}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    # print(data)
    releases = data["recordings"][0]["releases"]
    year = '?'
    # TODO: don't just pick the first release in the list.
    #   maybe find the minimum date?
    #   maybe filter out bad properties (live, re-recording)
    for release in releases:
        if "release-events" in release:
            date = release["release-events"][0]["date"]
            year = int(re.match("^\d{4}", date).group(0))
            break
    
    payload = {'artist': artist, 'name': title, 'year': year}
    print(payload)
    return payload


if __name__ == '__main__':
    app.run(debug=True)
