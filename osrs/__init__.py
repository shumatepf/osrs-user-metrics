import os
import random
import time
from flask import Flask
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime

from osrs import settings
import json
import logging

url = f"http://{settings.HOST}:{settings.PORT}"
print(url)
#client = InfluxDBClient(settings.HOST, settings.PORT)
client = InfluxDBClient(url=url, database=settings.DB_NAME)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

from osrs.cron import scheduler

logging.basicConfig(filename=settings.LOG_NAME,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)



def create_app():
    app = Flask(__name__)

    from osrs.routes import query, index

    app.register_blueprint(query, url_prefix="/search")
    app.register_blueprint(index, url_prefix="")

    # client.create_database(settings.DB_NAME)
    # client.switch_database(settings.DB_NAME)

    scheduler.init_app(app)
    scheduler.start()

    return app