# Recently Added on Plex

## A customapi widget for Homepage (https://gethomepage.dev/) that displays recently-added Movies and TV Shows on Plex.

![picture](https://i.imgur.com/umopaWL.png)

# Requirements
 - Python
 - Docker
 - Docker Compose

# Setup
1. Clone _**recently-added**_ to your Docker installation location:

2. Edit the information within _**recently-added.py**_:

    ```python
     # Define the variables
     PLEX_IP = "your_plex_ip"
     PLEX_PORT = "your_plex_port"
     PLEX_TOKEN = "your_plex_token"
     LIBRARY_TYPES = "movie,show,anime,4K"  # Comma-separated list of library types to create endpoints for
## Note: 
  - Find your Plex Token: _**https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/**_

# Installation

3. Start up application by running <code>docker-compose up -d</code>

## Note:
- Container creates API with a JSON output that can be used by Homepage.
- API accessible at _**<code>http://{IP}:4321/api/{endpoint}</code>**_

# Homepage Widget
4. Add to _**custom.css**_:

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
5. Add the widget to _**services.yaml**_:

    ```yaml
      - {NAME}
          id: #ABC123
          icon: {icon path}
          widget:
            type: customapi
            url: http://{IP}:4321/api/{endpoint}
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
## Note:
  - You can use <code>date_added</code> as the first field, and <code>title</code> in the <code>additionalField</code>, if you prefer.
  - Script supports 50 most recently added items per library, sorted from most recent <code>0</code> to earliest <code>49</code>.
  - This limit can be changed in the script.
    ```python
    recent_items = sorted_items[:50]
# Acknowledgements:
Special thanks to **haytada**, **MountainGod**, and **Plancke** in the Homepage Discord for all their help in making this happen! 