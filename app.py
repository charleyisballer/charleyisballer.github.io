from cs50 import SQL
from flask import Flask, redirect, render_template, request
from helpers import get_game_data

app = Flask(__name__)

game_data = SQL("sqlite:///game_data.db")

game_data.execute(
    "DELETE FROM champions"
)

active_player = get_game_data()["activePlayer"]
all_players = get_game_data()["allPlayers"]

for player in all_players:
    game_data.execute(
        "INSERT INTO champions (summoner_name, champion_name) VALUES (?, ?);",
        player["summonerName"],
        player["championName"])
    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        redirect("/champions")

    return render_template("index.html")

@app.route("/champions", methods=["GET", "POST"])
def champions():
    summoners = game_data.execute(
        "SELECT summoner_name FROM champions;"
    )
    champions = game_data.execute(
        "SELECT champion_name FROM champions"
    )
    names = zip(summoners, champions)

    return render_template("champions.html", names=names)