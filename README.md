# Recently Added on Plex

## A customapi widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows for Plex.

![picture](https://i.imgur.com/umopaWL.png)

### Requirements:
 - Python
 - Docker
 - Docker Compose

### Initial Setup:
1. Clone the contents of either the Movies or TV Shows folders (or both).
2. Edit the information within movie.py/tv.py with your Plex Media Server (PMS) IP Address, PMS Library Section ID and Plex Token
     - Find your authentication token / X-Plex-Token: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
     - Find your Plex Section ID: http://[PMS_IP_Address]:32400/library/sections?X-Plex-Token=[YourTokenGoesHere]

### Installation:
1. Move folder/s containing Dockerfile, requirements.txt, and script to a folder in Docker.
2. Navigate into the folder.
3. Build the image: _docker build -t (app name) ._
4. Create docker-compose.yml (or add to existing Homepage docker-compose.yml):

    ```yaml
    version: "3.3"
    services:
      (app name):
        container_name: (container name)
        ports:
          - (port):8080
        image: (app name)
        environment:
          - TZ=(timezone)
        networks:
          - (network name)
    networks:
      (network name):
        external: true
5. Build container: *docker-compose up -d*

Note: This should create an API with a JSON output that can be used by Homepage. The API should be available at _http://(IP):(port)/(api endpoint specified in the script)_
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
2. Add the widget to Homepage:

    ```yaml
      - <Widget Name>
          id: #ABC123
          widget:
            type: customapi
            url: <API URL>
            display: list
            mappings:
              - field:
                  0: title
                additionalField:
                  field:
                    0: date_added
                  color: theme
                  format: date
              - field:
                  1: title
                additionalField:
                  field:
                    1: date_added
                  color: theme
                  format: date
Note: Script supports up to 20 most recently added Movies and TV Shows, sorted from most recent to earliest. This limit can be changed in the scripts.

Special thanks to haytada and Plancke in the Homepage Discord for all their help in making this happen! 