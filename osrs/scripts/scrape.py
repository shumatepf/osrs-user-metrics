from bs4 import BeautifulSoup

import math
from scripts.errors import BadHiScoresPage, RequestFailed, UserNotFound
import settings

import asyncio
import aiohttp
import logging


def get_users(users):
    """
    Get users' stats concurrently
    """
    return asyncio.run(get_users_sync(users))


async def get_users_sync(users):
    """
    Asyncio event loop harness for getting users' stats
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, user in enumerate(users):
            tasks.append(asyncio.ensure_future(
                get_user(session, user, i * 0.1)))

        user_data = await asyncio.gather(*tasks)
        # remove any empty responses
        user_data_filtered = list(filter(lambda item: item is not None, user_data))
        return user_data_filtered


async def get_user(session, name, delay):
    """
    Get single user's stats coroutine
    """
    await asyncio.sleep(delay)
    url_formatted = settings.URL_API.format(name)

    async with session.get(url_formatted) as user_data:
        if user_data.status == 404:
            logging.warning(f"Username: {name} not found, skipping...")
            return None
        raw_stats = await user_data.text()
        skill_dict = {
            "measurement": "user_skills",
            "tags": {
                "name": name
            },
            "fields": normalize_stats(raw_stats)
        }
        return skill_dict


def normalize_stats(stats_raw):
    """
    Stats as space/comma separated values to dict
    """
    ssv = stats_raw.splitlines()
    stats_skills = {skill: int(ssv[i+1].split(',')[2])
                    for i, skill in enumerate(settings.SKILLS)}

    return stats_skills


def get_usernames(random_ranks):
    """
    Get usernames based on list of ranks from the hiscores html pages concurrently
    """
    return asyncio.run(get_usernames_sync(random_ranks))


async def get_usernames_sync(random_ranks):
    """
    Asyncio event loop harness for getting usernames
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, rank in enumerate(random_ranks):
            tasks.append(asyncio.ensure_future(
                get_page(session, rank, i * 0.4)))
        username_list = await asyncio.gather(*tasks)
        return username_list


async def get_page(session, rank, delay):
    """
    Get single username from hiscores page coroutine
    """
    await asyncio.sleep(delay)

    page_num = math.ceil(rank / 25)
    index = (rank - 1) % 25
    async with session.get(settings.URL_HTML, params={'table': 0, 'page': page_num}, timeout=30) as response:
        # NEED TO CHECK IF PAGE IS IP BLOCKED
        page = await response.text()
        return get_username_from_page(page, index)


def get_username_from_page(page, index):
    """
    Parse html page to find user at index
    """
    page_soup = BeautifulSoup(page, "html.parser")
    # if "your IP has been temporarily blocked" in page_soup:
    #         raise RequestFailed("blocked temporarily due to high usage")
    # NEED A TRY CATCH HERE -> Raise exception with page_num, index
    try:
        table = page_soup.find(id='contentHiscores').find("table").find("tbody")
        rows = table.find_all('tr')
        rows.pop(0)  # first row is always empty
        row = rows[index].find("a").text
        name = row.replace("\u00a0", " ")

        return name
    except:
        raise BadHiScoresPage(page_soup)
