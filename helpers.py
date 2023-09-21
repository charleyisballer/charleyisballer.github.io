import datetime
import os
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

def get_champion_data():
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json"

    # query API
    response = requests.get(
        url,
        verify=False
    )
    return response.json()

def get_champion_icons(champion):
    url = f"http://ddragon.leagueoflegends.com/cdn/13.18.1/img/champion/{champion}.png"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # save image
            image_name = f"{champion}.png"
            folder_name = "static/champion_icons"
            with open(os.path.join(folder_name, image_name), "wb") as f:
                f.write(response.content)
        else:
            print(f"HTTP GET request failed with status code {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_item_icons(item_id):
    if item_id == 0:
        return
    url = f"http://ddragon.leagueoflegends.com/cdn/13.18.1/img/item/{item_id}.png"
    response = requests.get(url)
    image_name = f"{item_id}.png"
    folder_name = "static/item_icons"
    with open(os.path.join(folder_name, image_name), "wb") as f:
        f.write(response.content)

def get_match_info_by_id(region, match_id, api_key):
    if region in ['NA']:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_summoner_by_username(region, summoner_id, api_key):
    url = f"https://{region}1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_summoner_by_puuid(region, puuid, api_key):
    url = f"https://{region}1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_summoner_history(puuid, region, api_key):
    if region in ['NA']:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}"
    response = requests.get(url)
    return response.json()



url = 'https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4767732253?api_key=RGAPI-3fe0c773-c6d2-4c2f-a39e-32dd0baf1324'
response = requests.get(url)
response = response.json()
print(response["metadata"]["matchId"])

    
