import os
import random
import time
from flask import Flask
from influxdb import InfluxDBClient

from datetime import datetime

import osrs.settings as settings
import json
import logging

client = InfluxDBClient(settings.HOST, settings.PORT)
from osrs.cron import scheduler

logging.basicConfig(filename=settings.LOG_NAME,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)



def create_app():
    app = Flask(__name__)

    from osrs.routes import query

    app.register_blueprint(query, url_prefix="/search")

    client.create_database(settings.DB_NAME)
    client.switch_database(settings.DB_NAME)

    scheduler.init_app(app)
    scheduler.start()

    return app