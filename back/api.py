#!/usr/bin/env python
# encoding: utf-8

import json

from flask import Flask

app = Flask(__name__)

@app.route("/")
def summary():
	with open("summary.tmp") as f:
		summary = json.loads(f.read())
	return summary
