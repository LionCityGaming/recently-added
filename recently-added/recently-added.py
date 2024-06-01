from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Define the variables
PLEX_IP = "your_plex_ip"
PLEX_PORT = "your_plex_port"
PLEX_TOKEN = "your_plex_token"
# Comma-separated list of library types to create endpoints for (e.g. movie,show,anime)
LIBRARY_TYPES = "your_plex_libraries"  

# Convert LIBRARY_TYPES to a list
LIBRARY_TYPES_LIST = [lib_type.strip() for lib_type in LIBRARY_TYPES.split(',')]

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

def create_recent_endpoint(item_type):
    def recent_items():
        libraries = get_libraries()
        if item_type == 'anime':
            lib_keys = [lib['key'] for lib in libraries if 'anime' in lib['title'].lower()]
        else:
            lib_keys = [lib['key'] for lib in libraries if lib['type'] == item_type]
        
        recent_data = []
        for lib_id in lib_keys:
            recent_data.extend(get_recent_items(lib_id, 'show' if item_type == 'anime' else item_type))
        
        if recent_data:
            formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_data]
            return jsonify(formatted_items)
        else:
            return jsonify({"message": f"No recent {item_type}s found."}), 404
    return recent_items

# Create dynamic endpoints based on LIBRARY_TYPES
for lib_type in LIBRARY_TYPES_LIST:
    endpoint = f'/api/recent_{lib_type}'
    view_func = create_recent_endpoint(lib_type)
    app.add_url_rule(endpoint, endpoint, view_func)

@app.route('/api/recent_items')
def recent_items():
    libraries = get_libraries()
    combined_output = {}
    for lib_type in LIBRARY_TYPES_LIST:
        if lib_type == 'anime':
            lib_keys = [lib['key'] for lib in libraries if 'anime' in lib['title'].lower()]
        else:
            lib_keys = [lib['key'] for lib in libraries if lib['type'] == lib_type]
        
        recent_data = []
        for lib_id in lib_keys:
            recent_data.extend(get_recent_items(lib_id, 'show' if lib_type == 'anime' else lib_type))
        
        formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_data]
        combined_output[lib_type] = formatted_items

    return jsonify(combined_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
