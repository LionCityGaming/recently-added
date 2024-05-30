# Recently Added on Plex

## A customapi widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows on Plex.

![picture](https://i.imgur.com/umopaWL.png)

### Requirements:
 - Python
 - Docker
 - Docker Compose

### Initial Setup:
1. Clone _**recently-added**_ to your Docker installation location:
    - Dockerfile
    - requirements.txt
    - recently-added.py
    - dockercompose.yml

2. Edit the information within _**recently-added.py**_:

    ```python
     # Define the variables
     PLEX_IP = "your_plex_ip"
     PLEX_PORT = "your_plex_port"
     MOVIE_LIBRARY_ID = "your_movie_library_id"
     TV_LIBRARY_ID = "your_tv_library_id"
     PLEX_TOKEN = "your_plex_token"
### Note: 
  - Find your authentication token / X-Plex-Token:

    _**https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/**_

  - Find your Plex Section IDs: 

    _**http://{your_plex_ip}:{your_plex_port}/library/sections?X-Plex-Token={your_plex_token}**_

### Installation:
3. Build the image:

   <code>docker build -t recently-added .</code>

4. Edit _**docker-compose.yml**_:

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
5. Build container:

   <code>docker-compose up -d</code>

### Note:
- This container creates APIs with a JSON output that can be used by Homepage.
- The APIs should be accessible at _**http://{IP}:{port}/api/{api endpoint}**_
   - Movies API Endpoint: _**get_recent_movies**_
   - TV Shows API Endpoint: _**get_recent_shows**_

### Homepage Widget:
6. Add to _**custom.css**_:

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
7. Add the widget to _**services.yaml**_:

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
  - You can use <code>date_added</code> as the first field, and <code>title</code> in the <code>additionalField</code>, if you prefer.
  - Script supports 50 most recently added Movies and TV Shows, sorted from most recent <code>0</code> to earliest <code>49</code>.
  - This limit can be changed in the script.

### Acknowledgement:
Special thanks to **haytada**, **MountainGod**, and **Plancke** in the Homepage Discord for all their help in making this happen! 