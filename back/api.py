#!/usr/bin/env python
# encoding: utf-8

import json
from os.path import isfile

from flask import Flask, jsonify

app = Flask(__name__)

FPATH = "summary.tmp"


@app.route("/")
def home():
    return "I Am Alive And I Am Not Alone"


@app.route("/summary")
def summary():
    if not isfile(FPATH):
        summary = {
            "summary": {
                "renegade_perc": 0.5,
                "renegade": 0,
                "paragon": 0,
                "alignment": "neutral"
            }
        }
    else:
        with open(FPATH) as f:
            summary = json.loads(f.read())
    return jsonify(summary)
