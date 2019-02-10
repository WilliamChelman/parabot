#!/usr/bin/env python
# encoding: utf-8
"""
Parabot.

Usage:
  parabot.py <config> [-u]
  parabot.py -h  | --help

Options:
  -u           No time limit between votes.
  -h --help    Show this screen.
"""

import configparser
import json
import logging
import sys
from datetime import datetime, timedelta

from docopt import docopt
from irc.bot import SingleServerIRCBot


def _get_logger():
    logger_name = 'vbot'
    logger_level = logging.DEBUG
    log_line_format = '%(asctime)s | %(name)s - %(levelname)s : %(message)s'
    log_line_date_format = '%Y-%m-%dT%H:%M:%SZ'
    logger_ = logging.getLogger(logger_name)
    logger_.setLevel(logger_level)
    logging_handler = logging.StreamHandler(stream=sys.stdout)
    logging_handler.setLevel(logger_level)
    logging_formatter = logging.Formatter(
        log_line_format,
        datefmt=log_line_date_format
    )
    logging_handler.setFormatter(logging_formatter)
    logger_.addHandler(logging_handler)
    return logger_


logger = _get_logger()


class VBot(SingleServerIRCBot):
    VERSION = '1.0.0'

    def __init__(self, host, port, nickname, password, channel, unlimited):
        logger.debug(
            'VBot.__init__ (VERSION = %r, unlimited = %s)',
            self.VERSION,
            unlimited
        )
        SingleServerIRCBot.__init__(
            self,
            [(host, port, password)],
            nickname,
            nickname
        )
        self.channel = channel
        self.unlimited = unlimited
        self.viewers = []
        self.voters = {}
        self.votes = {
            "paragon": 0,
            "renegade": 0
        }
        self.renegade_perc = 0.5
        self.alignment = "neutral"

    def on_welcome(self, connection, event):
        logger.debug('VBot.on_welcome')
        connection.join(self.channel)

    def on_join(self, connection, event):
        logger.debug('VBot.on_join')
        nickname = self._parse_nickname(event.source)
        self.viewers.append(nickname)

    def on_part(self, connection, event):
        logger.debug('VBot.on_part')
        nickname = self._parse_nickname(event.source)
        self.viewers.remove(nickname)

    def on_pubmsg(self, connection, event):
        logger.debug('VBot.on_pubmsg')
        message = event.arguments[0]
        logger.debug('message = %r', message)
        message = message.strip().lower()
        if message in ["paragon", "renegade"]:
            sender = self._parse_nickname(event.source)
            self.send_vote(sender, message)

    def send_vote(self, voter, vote):
        if voter not in self.voters:
            self.accept_vote(voter, vote)
        else:
            next_vote = self.voters[voter]
            if datetime.now() > next_vote:
                self.accept_vote(voter, vote)
            else:
                self.refuse_vote(voter)

    def accept_vote(self, voter, vote):
        message = "{} a voté {} !".format(voter, vote)
        self.connection.privmsg(self.channel, message)
        self.voters[voter] = datetime.now() + timedelta(
            minutes=5
        )
        self.votes[vote] += 1
        self.check_votes()

    def refuse_vote(self, voter):
        message = (
            "Désolé {}, il y a un délai de 5 minutes "
            "entre chaque vote".format(voter)
        )
        self.connection.privmsg("#jtv", ".w {} {}".format(voter, message))

    def check_votes(self):
        paragon = self.votes["paragon"]
        renegade = self.votes["renegade"]
        self.renegade_perc = renegade / (renegade + paragon)
        prev_alignment = self.alignment
        if self.renegade_perc > 0.5:
            self.alignment = "renegade"
        elif self.renegade_perc < 0.5:
            self.alignment = "paragon"
        else:
            self.alignment = "neutral"
        if prev_alignment != self.alignment:
            message = "Shepard est maintenant {} !".format(self.alignment)
            self.connection.privmsg(self.channel, message)
        data = {
            "summary": {
                "renegade_perc": self.renegade_perc,
                "renegade": renegade,
                "paragon": paragon,
                "alignment": self.alignment
            }
        }
        with open("summary.tmp", "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def _parse_nickname(user_id):
        # nickname!username@nickname.tmi.twitch.tv
        return user_id.split('!', 1)[0]


def main():
    args = docopt(__doc__, version='ParaBot 1.0')
    config = configparser.ConfigParser()
    unlimited = args["-u"]
    config.read(args["<config>"])
    host = config["BOT"]["host"]
    port = int(config["BOT"]["port"])
    username = config["BOT"]["username"]
    password = config["BOT"]["password"]
    channel = config["BOT"]["channel"]
    bot = VBot(host, port, username, password, channel, unlimited)
    bot.start()


if __name__ == '__main__':
    main()
