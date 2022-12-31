import os
import random
import time
from flask import Flask, request
from influxdb import InfluxDBClient
from flask_apscheduler import APScheduler

from datetime import datetime
from scripts import scrape

import settings
import json
import logging

app = Flask(__name__)
scheduler = APScheduler()

logging.basicConfig(filename=settings.LOG_NAME,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

scheduler.init_app(app)
scheduler.start()

""" Sample measurement
{
    "measurement": "activity",
    "tags": {
        "name": "Friendless98"
    },
    "fields": {
        "attack": 123,
        "defence": 321,
        ...
    }
},
"""

client = InfluxDBClient(settings.HOST, settings.PORT)
client.create_database(settings.DB_NAME)
client.switch_database(settings.DB_NAME)


@app.route('/search', methods=['GET'])
def index():
    """
    Dump stuff in database
    """
    args = request.args

    name = args.get('name')

    if not name:
        return "Please provide a name"

    q_r = client.query(f'select * from user_skills;')
    # print(q_r)
    result = q_r.get_points(tags={'name': name})
    return list(result)


@app.route('/user', methods=['GET'])
def user():
    """
    Get osrs user info as json (not from db)
    """
    args = request.args

    name = args.get('name')

    if not name:
        return "Please provide a name"

    try:
        skill_dict = scrape.get_user(name)
    except:
        return "Please enter a valid user", 400

    return skill_dict


@app.route('/write')
def write():
    """
    Write user {name} to db
    TO BE DEPRICATED - TOO DANGEROUS
    """
    data = request.get_json()

    if not data["users"]:
        return "No users provided", 403

    users_dict = scrape.get_users(data["users"])

    client.write_points(users_dict)

    return users_dict


@scheduler.task('cron', minute='0', hour='3', day='*', month='*', day_of_week='*')
def scrape_all():
    """
    Reads list of users, scrapes their user data, and dumps into db
    Cron runs every day at 3:00 AM
    """

    logging.info(f"Beginning scraping at {datetime.now().ctime()}")

    if not os.path.exists(settings.USER_FILE):
        start = time.time()
        logging.info(f"{settings.USER_FILE} does not exist, beginning file creation...")

        try:
            random_ranks = random.sample(range(500000, 1000000), 1) # this needs to be replaced at the command line
            list_users = scrape.get_usernames(random_ranks) # this is a lot of http requests ...
            with open(settings.USER_FILE, "w") as f:
                json.dump(list_users, f)
        except Exception: # NEED BETTER EXCEPTION
            logging.info(f"{settings.USER_FILE} creation failed, aborting at {datetime.now().ctime()}")
            return "Failed" # ?? need a good exit method

        logging.info(f"{settings.USER_FILE} created in {time.time() - start} seconds")
        print(f"{settings.USER_FILE} created in {time.time() - start} seconds")

    with open(settings.USER_FILE) as f:
        start = time.time()
        users = json.load(f)
        print(f"file grabbed in {time.time() - start} seconds")

        start = time.time()
        users_dict = scrape.get_users(users) # this is a lot of http requests ...
        print(f"users data fetched in {time.time() - start} seconds")

        start = time.time()
        client.write_points(users_dict)
        print(f"data uploaded in {time.time() - start} seconds")

    #date = datetime.now().ctime()
    logging.info(f"Finished scraping at {datetime.now().ctime()}")

    return "Done" # ??

@app.route("/")
def nothing():
    scrape_all()
    return "Done"

if __name__ == "__main__":
    app.run()
