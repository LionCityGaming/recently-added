# recently-added

## A widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows for Plex.

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
1. Move Dockerfile, requirements.txt, and script to a folder in Docker (One each for Movies, and TV Shows).
2. Navigate into the folder.
3. Build the image: _docker build -t (app name)_
4. Create docker-compose.yml:

    ```{version: "3.3"
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

Note: This should create an API with a JSON output that can be used by Homepage. The api should be available at http://(IP):(port)/(api endpoint specified in the script)
  - Movies API Endpoint: *get_recent_movies*
  - TV Shows API Endpoint: *get_recent_shows*

### Homepage Widget:
1. Add to custom.css:

    ``` 
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

    ```
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