from flask import Flask, request
from influxdb import InfluxDBClient
from flask_apscheduler import APScheduler

from datetime import datetime
import osrs
import settings
import json
import logging

app = Flask(__name__)
scheduler = APScheduler()

#logging = logging.getLogger()
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
    print(q_r)
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
        skill_dict = osrs.get_user(name)
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

    users_dict = osrs.get_users(data["users"])

    client.write_points(users_dict)

    return users_dict


@scheduler.task('cron', minute='0', hour='3', day='*', month='*', day_of_week='*')
def scrape():
    """
    Reads list of users, scrapes their user data, and dumps into db
    Cron runs every day at 3:00 AM
    """

    date = datetime.now().ctime()
    logging.info("Beginning scraping at " + date)

    with open('users.json') as f:
        users = json.load(f)
        users_dict = osrs.get_users(users)
        client.write_points(users_dict)
    
    date = datetime.now().ctime()
    logging.info("Finished scraping at " + date)

    return True


if __name__ == "__main__":
    app.run()
