#!/usr/bin/env python
# encoding: utf-8

from threading import Thread

from flask import Flask, jsonify

from parabot.ircbot import VBot

app = Flask(__name__)
PARABOT = None
RUNNING_PARABOT = False


def start_parabot():
    global PARABOT
    if PARABOT is None:
        unlimited = app.config["UNLIMITED"]
        host = app.config["HOST"]
        port = app.config["PORT"]
        username = app.config["USERNAME"]
        password = app.config["PASSWORD"]
        channel = app.config["CHANNEL"]
        PARABOT = VBot(host, port, username, password, channel, unlimited)
    PARABOT.start()


@app.route("/")
def home():
    return "I Am Alive And I Am Not Alone"


@app.route("/run_parabot")
def run_parabot():
    global RUNNING_PARABOT
    global PARABOT
    if not RUNNING_PARABOT:
        t = Thread(target=start_parabot)
        t.start()
        RUNNING_PARABOT = True
        return("Parabot running.")
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
