import base64
from flask import request, json
from osrs import query_api
from osrs.routes import query

import pandas as pd

from osrs import settings


@query.route('/<name>/diff')
def gain_since(name):
    """
    Get exp gain by skill for last 
    """
    args = request.args
    fromDate = args.get('from')
    toDate = args.get('to')

    print("fromDate = ", fromDate)
    print("toDate = ", toDate)

    if not (fromDate or toDate):
        return "Please enter a valid total range", 400

    if not (name):
        return "Please enter a valid username", 400

    query = f'''
    from(bucket:"{settings.DB_NAME}")\
    |> range(start: -{fromDate}d, stop: -{int(fromDate) - 1}d)\
    |> filter(fn:(r) => r._measurement=="user_skills")\
    |> filter(fn:(r) => r.name=="{name}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    df_start = query_api.query_data_frame(org=settings.ORG, query=query).head()

    print(df_start)

    query = f'''
    from(bucket:"{settings.DB_NAME}")\
    |> range(start: -{toDate}d, stop: -{int(toDate) - 1}d)\
    |> filter(fn:(r) => r._measurement=="user_skills")\
    |> filter(fn:(r) => r.name=="{name}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''

    df_end = query_api.query_data_frame(org=settings.ORG, query=query).head()

    print(df_end)

    skill_diff = {}

    for skill in settings.SKILLS:
        skill_diff[skill] = df_end[skill][0] - df_start[skill][0]

    max_skill = max(skill_diff, key=skill_diff.get)

    print(f"Max skill: {max_skill} {skill_diff[max_skill]} ")

    return json.dumps(skill_diff, default=int)


@query.route('/<name>', methods=['POST'])
def time(name):
    """
    Dump users data points between times
    """

    data = request.get_json()

    fromDate = data['from']
    toDate = data['to']

    if not (fromDate or toDate):
        return "Please enter a valid total range", 400

    if not (name):
        return "Please enter a valid username", 400

    query = f'''
    from(bucket:"{settings.DB_NAME}")\
    |> range(start: -{fromDate}d, stop: -{toDate}d)\
    |> filter(fn:(r) => r._measurement=="user_skills")\
    |> filter(fn:(r) => r.name=="{name}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    #
    result = query_api.query_data_frame(org=settings.ORG, query=query)

    # need to pull head and tail for pie chart calculations
    # need to aggregate data for other charts (line chart next)

    print(result)

    # Add all skills
    # for skill in settings.SKILLS:
    #     axis.plot(result["_time"], result[skill], label=skill)

    return list(result)
