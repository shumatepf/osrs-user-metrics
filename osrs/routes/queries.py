from flask import request
from osrs import client
from osrs.routes import query

@query.route('/', methods=['GET'])
def index():
    """
    Dump stuff in database
    """
    args = request.args

    name = args.get('name')

    if not name:
        return "Please provide a name"

    q_r = client.query(f"""select * from user_skills where "name"='{name}';""")
    #result = q_r.get_points(tags={'name': name})
    return list(q_r)
