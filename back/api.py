#!/usr/bin/env python
# encoding: utf-8

from parabot import VBot

from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.ini')
unlimited = app.config["UNLIMITED"]
host = app.config["HOST"]
port = app.config["PORT"]
username = app.config["USERNAME"]
password = app.config["PASSWORD"]
channel = app.config["CHANNEL"]
PARABOT = VBot(host, port, username, password, channel, unlimited)
RUNNING_PARABOT = False


@app.route("/")
def home():
    return "I Am Alive And I Am Not Alone"


@app.route("/run_parabot")
def run_parabot():
    global RUNNING_PARABOT
    global PARABOT
    if not RUNNING_PARABOT:
        RUNNING_PARABOT = True
        PARABOT.start()
    else:
        return("Parabot already running.")


@app.route("/stop_parabot")
def stop_parabot():
    global RUNNING_PARABOT
    global PARABOT
    if not RUNNING_PARABOT:
        return("Parabot not running.")
    else:
        PARABOT.connection.disconnect()
        PARABOT.reset_votes()
        RUNNING_PARABOT = False
        return("Parabot stopped.")


@app.route("/summary")
def summary():
    if not RUNNING_PARABOT:
        return("Parabot not running.")
    else:
        return jsonify(PARABOT.get_summary())
