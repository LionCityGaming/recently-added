from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

def get_recent_shows(url):
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        sorted_data = sorted(data['MediaContainer']['Metadata'], key=lambda x: int(x['addedAt']), reverse=True)
        recent_data = sorted_data[:20]  # Take only the 20 most recently added items
        recent_shows = [{"title": item['title'], "date_added": format_date(item['addedAt'])} for item in recent_data]
        return recent_shows
    else:
        return []

def format_date(timestamp):
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%b %Oe")

@app.route('/api/recent_shows')
def recent_shows():
    plex_url = "http://<IP>:<Port>/library/sections/<movie section ID>/all?X-Plex-Token=<Plex Token>"
    recent_shows = get_recent_shows(plex_url)
    if recent_shows:
        return jsonify(recent_shows)
    else:
        return jsonify({"error": "No recent shows found."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
