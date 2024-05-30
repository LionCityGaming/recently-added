# Recently Added on Plex

## A customapi widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows for Plex.

![picture](https://i.imgur.com/umopaWL.png)

### Requirements:
 - Python
 - Docker
 - Docker Compose

### Initial Setup:
1. Clone the recently-added folder.
2. Edit the information within recently-added.py.

    ```python
       # Define the variables
       PLEX_IP = "your_plex_ip"
       PLEX_PORT = "your_plex_port"
       MOVIE_LIBRARY_ID = "your_movie_library_id"
       TV_LIBRARY_ID = "your_tv_library_id"
       PLEX_TOKEN = "your_plex_token"
  - Find your authentication token / X-Plex-Token: *https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/*
  - Find your Plex Section IDs: *http://{your_plex_ip}:{your_plex_port}/library/sections?X-Plex-Token={your_plex_token}*

### Installation:
1. Move folder (containing Dockerfile, requirements.txt, recently-added.py, and docker-compose.yml) to Docker install location.
2. Navigate into the folder.
3. Build the image: _docker build -t recently-added ._
4. Edit docker-compose.yml:

    ```yaml
    version: "3.3"
    services:
      recently-added:
        container_name: recently-added
        ports:
          - {port}:8080
        image: recently-added
        environment:
          - TZ={timezone}
        networks:
          - {network name}
    networks:
      {network name}:
        external: true
5. Build container: *docker-compose up -d*

### Note:
- This container creates APIs with a JSON output that can be used by Homepage.
- The APIs should be available at _http://{IP}:{port}/api/{api endpoint}_
   - Movies API Endpoint: *get_recent_movies*
   - TV Shows API Endpoint: *get_recent_shows*

### Homepage Widget:
1. Add to custom.css:

    ```css 
    #ABC123>div>div.relative.flex.flex-row.w-full.service-container {
    &>div>div {
        display: block;
        text-align: left; /* Adjusted to align all elements left */

        &>div.flex.flex-row.text-right {

            &>div:nth-child(1) {
                text-align: left; /* Adjusted to align left */
                margin-left: .5rem;
            }

            &>div:nth-child(2) {
                text-align: left; /* Adjusted to align left */
                margin-left: auto;
            }
2. Add the widget to Homepage (You can use "date_added" as the first field, and "title" in the additionalField if you prefer):

    ```yaml
      - Recently Added Movies
          id: #ABC123
          widget:
            type: customapi
            url: http://{IP}:{port}/api/recent_movies
            display: list
            mappings:
              - field:
                  0: title
                additionalField:
                  field:
                    0: date_added
              - field:
                  1: title
                additionalField:
                  field:
                    1: date_added

      - Recently Added TV Shows
          id: #ABC123
          widget:
            type: customapi
            url: http://{IP}:{port}/api/recent_shows
            display: list
            mappings:
              - field:
                  0: title
                additionalField:
                  field:
                    0: date_added
              - field:
                  1: title
                additionalField:
                  field:
                    1: date_added
### Note:
  - Script supports 50 most recently added Movies and TV Shows, sorted from most recent (0) to earliest (49).
  - This limit can be changed in the script.

### Acknowledgement:
Special thanks to haytada, MountainGod, and Plancke in the Homepage Discord for all their help in making this happen! 