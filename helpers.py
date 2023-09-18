import datetime
import json
import requests
import time


def get_game_data():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"

    # query API
    while True:
        try:
            response = requests.get(
                url,
                verify=False
            )
            return response.json()
    
        except (requests.RequestException, ValueError, KeyError, IndexError):
            # Try again every 5 seconds
            print(f'{datetime.datetime.now()} | Not in Game rn')
            time.sleep(5)
            continue

active_player = get_game_data()["activePlayer"]
all_players = get_game_data()["allPlayers"]


    
