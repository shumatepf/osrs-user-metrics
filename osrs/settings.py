import os

HOST = os.getenv('HOST', 'localhost')
PORT = 8086

DB_NAME = os.getenv('DB_NAME', 'osrs_user_metrics')
LOG_NAME = os.getenv('LOG_NAME', 'logs.log')

TOKEN = os.getenv('INFLUXDB_TOKEN', 'nothing')
ORG= os.getenv('ORG', 'osrs')

USER_FILE = "users.json"

URL_API = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={}"
URL_HTML = "https://secure.runescape.com/m=hiscore_oldschool/overall"

# DO NOT CHANGE ORDER
SKILLS = ["attack", "defense", "strength", "hitpoints", "ranged", "prayer", "magic", "cooking", "woodcutting", "fletching", "fishing", "firemaking",
          "crafting", "smithing", "mining", "herblore", "agility", "thieving", "slayer", "farming", "runecrafting", "hunter", "construction"]
