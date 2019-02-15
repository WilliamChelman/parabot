#!/usr/bin/env python
# encoding: utf-8
"""
Parabot API server.
Usage:
  wsgi.py <config>
  parabot.py -h  | --help
Options:
  -h --help    Show this screen.
"""

# from docopt import docopt
from os.path import abspath
from sys import argv

import parabot.api as flask_app

app = flask_app.app
port = 5000


def main():
    # Docopt won't accept valid input.
    # args = docopt(__doc__)
    # app.config.from_pyfile(args["<config>"])
    if len(argv) < 2 or argv[1] == "-h":
        exit(__doc__)
    config = abspath(argv[1])
    app.config.from_pyfile(config)
    app.run(port=port)


if __name__ == '__main__':
    main()
