import os
import random
import time
import json

from datetime import datetime
from flask_apscheduler import APScheduler

from osrs import settings, logging, write_api
from osrs_lib import hiscores

scheduler = APScheduler()

@scheduler.task('cron', minute='*', hour='*', day='*', month='*', day_of_week='*')
def scrape_all():
    """
    Reads list of users, scrapes their user data, and dumps into db
    Cron runs every day at 3:00 AM
    """

    logging.info(f"Beginning scraping at {datetime.now().ctime()}")

    if not os.path.exists(settings.USER_FILE):
        logging.info("File not found, exiting...")
        return "Error: file 'users.json' does not exist"
        """start = time.time()
        logging.info(f"{settings.USER_FILE} does not exist, beginning file creation...")

        try:
            random_ranks = random.sample(range(500000, 700000), 1000) # this needs to be replaced at the command line
            list_users = scrape.get_usernames(random_ranks) # this is a lot of http requests ...
            list_users.append("Friendless98")
            list_users.append("treechopperr")
            with open(settings.USER_FILE, "w") as f:
                json.dump(list_users, f)
        except Exception as e: # NEED BETTER EXCEPTION
            logging.info(f"{e}")
            logging.info(f"{settings.USER_FILE} creation failed, aborting at {datetime.now().ctime()}")
            return "Failed" # ?? need a good exit method

        logging.info(f"{settings.USER_FILE} created in {time.time() - start} seconds")
        print(f"{settings.USER_FILE} created in {time.time() - start} seconds")"""

    with open(settings.USER_FILE) as f:
        start = time.time()
        users = json.load(f)
        print(f"file grabbed in {time.time() - start} seconds")

        start = time.time()
        users_dict = hiscores.get_stats(users) # this is a lot of http requests ...
        print(f"users data fetched in {time.time() - start} seconds")

        start = time.time()
        write_api.write(bucket=settings.DB_NAME, org="osrs", record=users_dict)
        print(f"data uploaded in {time.time() - start} seconds")

    logging.info(f"Finished scraping at {datetime.now().ctime()}")
    return "Done" # ??