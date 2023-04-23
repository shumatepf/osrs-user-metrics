from flask import request
from osrs import client
from osrs.routes import query
from datetime import datetime

from osrs import cron

@query.route('/dump', methods=['GET'])
def stupid():
    print("dump")
    return cron.scrape_all()

@query.route('/', methods=['GET'])
def name():
    """
    Dump user data
    """
    args = request.args

    name = args.get('name')

    if not name:
        return "Please provide a name", 400

    q_r = client.query(f"""select * from user_skills where "name"='{name}';""")
    return list(q_r)

@query.route('/time', methods=['GET'])
def time():
    """
    Dump users data between times
    """
    args = request.args
    start_raw = args.get('start')
    end_raw = args.get('end')
    name = args.get('name')
    name = name if name else '*'

    print(start_raw, end_raw)

    if not (start_raw or end_raw):
        return "Please enter a start and end date", 400
    
    try:
        start = datetime.strptime(start_raw, )
        """asd"""
    except Exception as e:
        return e

    q_r = client.query(f"""select * from user_skills where "name"='{name}';""")

    return list(q_r)