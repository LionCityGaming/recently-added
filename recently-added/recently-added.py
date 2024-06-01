from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Define the variables
PLEX_IP = "your_plex_ip"
PLEX_PORT = "your_plex_port"
PLEX_TOKEN = "your_plex_token"

def get_libraries():
    url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections?X-Plex-Token={PLEX_TOKEN}"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['MediaContainer']['Directory']
    else:
        print(f"Failed to fetch libraries: {response.status_code}")
        return []

def get_recent_items(library_id, item_type):
    url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{library_id}/all?X-Plex-Token={PLEX_TOKEN}"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        items = [item for item in data['MediaContainer']['Metadata'] if item['type'] == item_type]
        sorted_items = sorted(items, key=lambda x: int(x['addedAt']), reverse=True)
        recent_items = sorted_items[:50]  # Take only the 50 most recently added items
        return recent_items
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def format_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%b %d")

@app.route('/api/recent_movies')
def recent_movies():
    libraries = get_libraries()
    movie_libraries = [lib['key'] for lib in libraries if lib['type'] == 'movie']
    recent_movies_data = []
    for lib_id in movie_libraries:
        recent_movies_data.extend(get_recent_items(lib_id, 'movie'))
    if recent_movies_data:
        formatted_movies = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_movies_data]
        return jsonify(formatted_movies)
    else:
        return jsonify({"message": "No recent movies found."}), 404

@app.route('/api/recent_shows')
def recent_shows():
    libraries = get_libraries()
    show_libraries = [lib['key'] for lib in libraries if lib['type'] == 'show']
    recent_shows_data = []
    for lib_id in show_libraries:
        recent_shows_data.extend(get_recent_items(lib_id, 'show'))
    if recent_shows_data:
        formatted_shows = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_shows_data]
        return jsonify(formatted_shows)
    else:
        return jsonify({"error": "No recent shows found."}), 404

@app.route('/api/recent_items')
def recent_items():
    libraries = get_libraries()
    movie_libraries = [lib['key'] for lib in libraries if lib['type'] == 'movie']
    show_libraries = [lib['key'] for lib in libraries if lib['type'] == 'show']

    recent_movies_data = []
    for lib_id in movie_libraries:
        recent_movies_data.extend(get_recent_items(lib_id, 'movie'))

    recent_shows_data = []
    for lib_id in show_libraries:
        recent_shows_data.extend(get_recent_items(lib_id, 'show'))

    formatted_movies = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_movies_data]
    formatted_shows = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_shows_data]

    combined_output = {
        "movies": formatted_movies,
        "shows": formatted_shows
    }

    return jsonify(combined_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
