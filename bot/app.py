#!/usr/bin/env python

import logging
import os

from beepboop import resourcer
from beepboop import bot_manager

from slack_bot import SlackBot
from slack_bot import spawn_bot

from flask import Flask

logger = logging.getLogger(__name__)
server = Flask(__name__)

@server.route ('/toto', methods=['GET'])
def local_test():
    return Response('it works')


if __name__ == "__main__":
    port= os.getenv("PORT","not found")
    server.run(host='0.0.0.0',port=8080,debug=True)
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv("SLACK_TOKEN", "")
    logging.info("token: {}".format(slack_token))
    logging.info(port)

    if slack_token == "":
        logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")
        slack_token = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    else:
        # only want to run a single instance of the bot in dev mode
        bot = SlackBot(slack_token)
        bot.start({})
