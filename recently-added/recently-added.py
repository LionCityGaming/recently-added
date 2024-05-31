from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# Define the variables
PLEX_IP = "your_plex_ip"
PLEX_PORT = "your_plex_port"
MOVIE_LIBRARY_ID = "your_movie_library_id"
TV_LIBRARY_ID = "your_tv_library_id"
PLEX_TOKEN = "your_plex_token"

def get_recent_items(url, item_type = None):
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if not item_type:
            items = [item for item in data['MediaContainer']['Metadata']]
        else:
            items = [item for item in data['MediaContainer']['Metadata'] if item['type'] == item_type]
        sorted_items = sorted(items, key=lambda x: int(x['addedAt']), reverse=True)
        recent_items = sorted_items[:50]  # Take only the 50 most recently added items
        return recent_items
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def get_libraries() -> dict:
    libraries = {}
    plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections?X-Plex-Token={PLEX_TOKEN}"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(plex_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for lib in data['MediaContainer']['Directory']:
            libraries[lib['title']] = int(lib['key'])
        return libraries
    else:
        print(f"Failed to fetch libraries: {response.status_code}")
        return {}

def format_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%b %d")

@app.route('/api/recent', methods=['GET'])
def recent():
    data = request.get_json()
    libraries = get_libraries()
    formatted_items = []
    if data['library'] == 'all':
        for id in libraries.values():
            plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{id}/all?X-Plex-Token={PLEX_TOKEN}"
            recent_items_data = get_recent_items(plex_url)
            if recent_items_data:
                formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_items_data]
            else:
                return jsonify({"message": "No recent items found."}), 404
        return jsonify(formatted_items)
    elif ',' in data['library']:
        libs = str(data['library']).split(',')
        for lib in libs:
            plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{libraries[lib]}/all?X-Plex-Token={PLEX_TOKEN}"
            recent_items_data = get_recent_items(plex_url)
            if recent_items_data:
                formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_items_data]
            else:
                return jsonify({"message": "No recent items found."}), 404
        return jsonify(formatted_items)
    elif ',' not in data['library'] and not data['library'] == 'all':
        plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{libraries[data['library']]}/all?X-Plex-Token={PLEX_TOKEN}"
        recent_items_data = get_recent_items(plex_url)
        if recent_items_data:
            formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_items_data]
            return jsonify(formatted_items)
        else:
            return jsonify({"message": "No recent items found."}), 404
    else:
        return jsonify({"message": "No recent items found."}), 404

@app.route('/api/recent_movies')
def recent_movies():
    if not MOVIE_LIBRARY_ID == "your_movie_library_id":
        plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{MOVIE_LIBRARY_ID}/all?X-Plex-Token={PLEX_TOKEN}"
        recent_movies_data = get_recent_items(plex_url, 'movie')
        if recent_movies_data:
            formatted_movies = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_movies_data]
            return jsonify(formatted_movies)
        else:
            return jsonify({"message": "No recent movies found."}), 404
    else:
        return jsonify({"message": "MOVIE_LIBRARY_ID is not configured."}), 404

@app.route('/api/recent_shows')
def recent_shows():
    if not TV_LIBRARY_ID == "your_tv_library_id":
        plex_url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{TV_LIBRARY_ID}/all?X-Plex-Token={PLEX_TOKEN}"
        recent_shows_data = get_recent_items(plex_url, 'show')
        if recent_shows_data:
            formatted_shows = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_shows_data]
            return jsonify(formatted_shows)
        else:
            return jsonify({"error": "No recent shows found."}), 404
    else:
        return jsonify({"message": "TV_LIBRARY_ID is not configured."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)