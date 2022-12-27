from OSRSBytes import Hiscores
from datetime import datetime

import time
import asyncio
import aiohttp


# DO NOT CHANGE ORDER
skills = ["attack", "defense", "strength", "hitpoints", "ranged", "prayer", "magic", "cooking", "woodcutting", "fletching", "fishing", "firemaking",
          "crafting", "smithing", "mining", "herblore", "agility", "thieving", "slayer", "farming", "runecrafting", "hunter", "construction"]

url = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={}"


async def get_user(session, name, delay):
    await asyncio.sleep(delay)
    url_formatted = url.format(name)
    start = time.time()
    async with session.get(url_formatted) as user_data:
        if user_data.status == 404:
            return f"Username: {name} not found"
        raw_stats = await user_data.text()
        skill_dict = {
            "measurement": "user_skills",
            "tags": {
                "name": name
            },
            "fields": normalize_stats(raw_stats)
        }
        print("user {} xp fetch completed in {} seconds".format(name, time.time() - start))
        return skill_dict


def normalize_stats(stats_raw):
    ssv = stats_raw.splitlines()
    stats_skills = {skill: ssv[i+1].split(',')[2] for i, skill in enumerate(skills)}

    return stats_skills


async def get_users_sync(users):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, user in enumerate(users):
            tasks.append(asyncio.ensure_future(
                get_user(session, user, i * 0.1)))

        user_data = await asyncio.gather(*tasks)
        return user_data


def get_users(users):
    return asyncio.run(get_users_sync(users))
