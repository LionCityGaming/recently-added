# Recently Added on Plex

## A customapi widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows on Plex.
![picture](https://i.imgur.com/umopaWL.png)
## Requirements
 - Python
 - Docker
 - Docker Compose
## Setup
1. Clone to your Docker installation location

   <code>git clone https://github.com/LionCityGaming/recently-added.git</code>

2. Find your Plex Token

   https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token
## Configuration
3. Define variables within **.env**

    ```python
     PLEX_IP="your_plex_ip"
     PLEX_PORT="your_plex_port"
     PLEX_TOKEN="your_plex_token"
     LIBRARY_NAMES="your_plex_libraries"
     # Comma-separated list of library names to create endpoints for (e.g. LIBRARY_NAMES="Movies,TV Shows,Anime")
## Installation

4. Start up application

   <code>docker-compose up -d</code>

---
_**NOTE**_

- API accessible at _http://{IP}:4321/api/{endpoint}_
  - replace all spaces in library names with an underscore <code>_</code> in endpoint

  - Example: _http://{IP}:4321/api/tv_shows_

- API for all recent items in all libraries accesible at _http://{IP}:4321/api/all_
---
## Homepage Widget
5. Add to **custom.css**:

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
6. Add to **services.yaml**:

    ```yaml
    - Widget Name:
        icon: icon.png
        id: ABC123
        widget:
          type: customapi
          url: http://{IP}/api/{endpoint}
          method: GET
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
---
_**NOTE**_
  - You can use <code>date_added</code> as the first field, and <code>title</code> in the <code>additionalField</code>, if you prefer.

  - Script supports 50 most recently added items per library, sorted from most recent <code>0</code> to earliest <code>49</code>.

  - This limit can be changed in the script.
    ```python
    recent_items = sorted_items[:50]
---
# Acknowledgements:

Special thanks for all their help in making this happen!

- **haytada**
- **MountainGod**
- **Plancke**
