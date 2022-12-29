from bs4 import BeautifulSoup

import math
import settings

import asyncio
import aiohttp


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
        return user_data


async def get_user(session, name, delay):
    """
    Get single user's stats coroutine
    """
    await asyncio.sleep(delay)
    url_formatted = settings.URL.format(name)

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
        return skill_dict


def normalize_stats(stats_raw):
    """
    Stats as space/comma separated values to dict
    """
    ssv = stats_raw.splitlines()
    stats_skills = {skill: ssv[i+1].split(',')[2]
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
                get_page(session, rank, i * 0.1)))
        username_list = await asyncio.gather(*tasks)
        return username_list


async def http_request(session, params):
    """
    http interface for getting html pages
    """
    async with session.get(settings.URL_HTML, params=params) as response:
        page = await response.text()
        return page


async def get_page(session, rank, delay):
    """
    Get single username from hiscores page coroutine
    """
    await asyncio.sleep(delay)

    page_num = math.ceil(rank / 25)
    index = (rank - 1) % 25
    page = await http_request(session, {'table': 0, 'page': page_num})
    return get_username_from_page(page, index)


def get_username_from_page(page, index):
    """
    Parse html page to find user at index
    """
    page_soup = BeautifulSoup(page, "html.parser")
    table = page_soup.find(id='contentHiscores').find("table").find("tbody")
    rows = table.find_all('tr')
    rows.pop(0)  # first row is always empty
    row = rows[index].find("a").text
    name = row.replace("\u00a0", " ")

    return name
