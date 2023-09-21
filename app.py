from cs50 import SQL
from flask import Flask, redirect, render_template, request
from helpers import get_game_data, get_champion_data, get_champion_icons, get_item_icons, get_summoner_by_puuid, get_summoner_by_username, get_summoner_history, get_match_info_by_id
import os
import urllib3

urllib3.disable_warnings()
app = Flask(__name__)

game_data = SQL("sqlite:///game_data.db")

game_data.execute(
    "DELETE FROM champions"
)

api_key = "RGAPI-3fe0c773-c6d2-4c2f-a39e-32dd0baf1324"

active_player = get_game_data()["activePlayer"]
all_players = get_game_data()["allPlayers"]
champion_data = get_champion_data()

for player in all_players:
    game_data.execute(
        "INSERT INTO champions (summoner_name, champion_name, level, kills, deaths, assists, creepscore) VALUES (?, ?, ?, ?, ?, ?, ?);",
        player["summonerName"],
        player["championName"],
        player["level"],
        player["scores"]["kills"],
        player["scores"]["deaths"],
        player["scores"]["assists"],
        player["scores"]["creepScore"],
        )
    

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/champions", methods=["GET", "POST"])
def champions():
    summoners = game_data.execute(
        "SELECT summoner_name FROM champions;"
    )
    champions = game_data.execute(
        "SELECT champion_name, level, kills, deaths, assists, creepscore FROM champions"
    )

    for champion in champions:
        champion_name = champion["champion_name"].replace(' ', '')
        if champion_name == "Cho'Gath":
            champion_name = "Chogath"

        get_champion_icons(champion_name)
        champion["champ_img"] = champion_name
    names = zip(summoners, champions)
    folder = "static/champion_icons"
    images_len = len([f for f in os.listdir(folder) if f.endswith('.png')])

    return render_template("champions.html", names=names, images_len=images_len)

@app.route("/summoner", methods=["GET", "POST"])
def summoner():
    if request.method == "POST":

        # reset database
        game_data.execute("DELETE FROM match;")

        # get simple data like region, summoner_id (Username)
        region = request.form.get("region")
        summoner_id = request.form.get("summoner_id")

        # request more data on the summoner (puuid, and more)
        summoner_info = get_summoner_by_username(region, summoner_id, api_key)

        # assign puuid variable to make things easier
        puuid = summoner_info["puuid"]

        # pull the match history by game id using API
        match_history_by_id = get_summoner_history(puuid, region, api_key)

        # create empty list for match_history with all data to go in
        match_history = []

        # add the most recent match to this list
        match_history.append(get_match_info_by_id(region, match_history_by_id[0], api_key))

        # go through each match in match_history list
        for match_id in match_history:
            match = match_id["metadata"]["matchId"]
            game_mode = match_id["info"]["gameMode"]

            # grab each participant
            for participant in match_id["info"]["participants"]:
                
                # get their summoner name
                summoner_name  = participant["summonerName"]

                # get their champion played
                champion_played = participant["championName"]

                # get their score
                level = participant["champLevel"]
                kills = participant["kills"]
                assists = participant["assists"]
                deaths = participant["deaths"]
                creepscore = participant["totalMinionsKilled"]
                puuid = "poop"
                team_id = participant["teamId"]

                # get item information
                items = {}
                for i in range(7):
                    items[f"item{i}"] = participant[f"item{i}"]
                    get_item_icons(items[f"item{i}"])



                # add to the database with match id as well
                game_data.execute(
                    "INSERT INTO match VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    summoner_name,
                    champion_played,
                    level,
                    kills,
                    deaths,
                    assists,
                    creepscore,
                    puuid,
                    match,
                    team_id,
                    game_mode,
                    items["item0"],
                    items["item1"],
                    items["item2"],
                    items["item3"],
                    items["item4"],
                    items["item5"],
                    items["item6"]
                )

                

                

        players = game_data.execute("SELECT * FROM match;")

        for player in players:
                    champion_name = player["champion_name"].replace(' ', '')
                    if champion_name == "Cho'Gath":
                        champion_name = "Chogath"

                    get_champion_icons(champion_name)
                    player["champ_img"] = champion_name
                    
                         

            

        return render_template("summoner.html", summoner_id=summoner_id, players=players)

    return render_template("summoner.html")