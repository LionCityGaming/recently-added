from flask import Flask, jsonify
import requests
from datetime import datetime
import json

app = Flask(__name__)

def get_recent_movies(url):
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movies = [item for item in data['MediaContainer']['Metadata'] if item['type'] == 'movie']
        sorted_movies = sorted(movies, key=lambda x: int(x['addedAt']), reverse=True)
        recent_movies = sorted_movies[:20]  # Take only the 20 most recently added movies
        return recent_movies
    else:
        print("Failed to fetch data:", response.status_code)
        return []

def format_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%b %Oe")

@app.route('/api/recent_movies')
def recent_movies():
    plex_url = "http://<IP>:<Port>/library/sections/<library ID>/all?X-Plex-Token=<Plex Token>"
    recent_movies_data = get_recent_movies(plex_url)
    if recent_movies_data:
        formatted_movies = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_movies_data]
        return jsonify(formatted_movies)
    else:
        return jsonify({"message": "No recent movies found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
