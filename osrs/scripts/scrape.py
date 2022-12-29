import settings

import asyncio
import aiohttp

async def get_user(session, name, delay):
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
    ssv = stats_raw.splitlines()
    stats_skills = {skill: ssv[i+1].split(',')[2] for i, skill in enumerate(settings.SKILLS)}

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
