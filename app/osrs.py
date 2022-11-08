from OSRSBytes import Hiscores
from datetime import datetime

skills = ["attack", "strength", "defense", "ranged", "prayer", "magic", "runecrafting", "hitpoints", "crafting", "mining", "smithing", "fishing",
          "cooking", "firemaking", "woodcutting", "agility", "herblore", "thieving", "fletching", "slayer", "farming", "construction", "hunter"]


def get_user(name):
    user_data = Hiscores(name)
    skill_dict = {skill: user_data.skill(skill, 'experience')
                  for skill in skills}

    return skill_dict


def get_users(names):
    users_list = []
    for name in names:
        skill_dict = {
            "measurement": "user_skills",
            "tags": {
                "name": name
            },
            "time": datetime.now(),
            "fields": get_user(name)
        }
        # get_user(name)
        users_list.append(skill_dict)

    return users_list
