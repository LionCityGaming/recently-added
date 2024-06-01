from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Define the variables
PLEX_IP = "your_plex_ip"
PLEX_PORT = "your_plex_port"
PLEX_TOKEN = "your_plex_token"
# Comma-separated list of library names to create endpoints for (e.g. Movies,Shows,Anime)
LIBRARY_NAMES = "your_plex_libraries"  

# Convert LIBRARY_NAMES to a list
LIBRARY_NAMES_LIST = [lib_name.strip() for lib_name in LIBRARY_NAMES.split(',')]

def get_libraries():
    url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections?X-Plex-Token={PLEX_TOKEN}"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['MediaContainer']['Directory']
    else:
        print(f"Failed to fetch libraries: {response.status_code}")
        return []

def get_recent_items(library_id):
    url = f"http://{PLEX_IP}:{PLEX_PORT}/library/sections/{library_id}/all?X-Plex-Token={PLEX_TOKEN}"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        items = data['MediaContainer'].get('Metadata', [])
        sorted_items = sorted(items, key=lambda x: int(x['addedAt']), reverse=True)
        recent_items = sorted_items[:50]  # Take only the 50 most recently added items
        return recent_items
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def format_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%b %d")

def create_recent_endpoint(library_name):
    def recent_items():
        libraries = get_libraries()
        lib_keys = [lib['key'] for lib in libraries if lib['title'].lower() == library_name.lower()]
        
        if not lib_keys:
            return jsonify({"message": f"No library found with the name {library_name}."}), 404
        
        recent_data = []
        for lib_id in lib_keys:
            recent_data.extend(get_recent_items(lib_id))
        
        if recent_data:
            formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_data]
            return jsonify(formatted_items)
        else:
            return jsonify({"message": f"No recent items found in {library_name} library."}), 404
    return recent_items

# Create dynamic endpoints based on LIBRARY_NAMES
for lib_name in LIBRARY_NAMES_LIST:
    endpoint = f'/api/{lib_name.lower().replace(" ", "_")}'
    view_func = create_recent_endpoint(lib_name)
    app.add_url_rule(endpoint, endpoint, view_func)

@app.route('/api/all')
def all_items():
    libraries = get_libraries()
    combined_output = {}
    for lib_name in LIBRARY_NAMES_LIST:
        lib_keys = [lib['key'] for lib in libraries if lib['title'].lower() == lib_name.lower()]
        
        recent_data = []
        for lib_id in lib_keys:
            recent_data.extend(get_recent_items(lib_id))
        
        formatted_items = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_data]
        combined_output[lib_name] = formatted_items

    return jsonify(combined_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
