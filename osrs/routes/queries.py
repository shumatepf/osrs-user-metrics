import base64
from flask import request, Response, json
from osrs import client, query_api
from osrs.routes import query
from datetime import timedelta, date
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from osrs import settings


@query.route('/', methods=['GET'])
def name():
    """
    Dump all of a user's data
    """
    args = request.args

    name = args.get('name')

    if not name:
        return "Please provide a name", 400

    query = f'''
    from(bucket:"{settings.DB_NAME}")\
    |> range(start: -20d)\
    |> filter(fn:(r) => r._measurement=="user_skills")\
    |> filter(fn:(r) => r.name=="{name}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    # 
    result = query_api.query_data_frame(org=settings.ORG, query=query)

    fig = Figure(figsize=(10,10))
    axis = fig.add_subplot()
    # Add all skills
    for skill in settings.SKILLS:
        axis.plot(result["_time"], result[skill], label=skill)

    print(result["hitpoints"])

    x_labels = [time.strftime('%m/%d') for time in result["_time"]]
    axis.set_xticklabels(x_labels)
    
    axis.ticklabel_format(axis='y', style='plain')
    axis.set_title(f"{name}'s skills for the last")
    axis.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    FigureCanvas(fig).print_png(buf)
    return Response(buf.getvalue(), mimetype='image/png')

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

@query.route('/<name>', methods=['GET'])
def time(name):
    """
    Dump users data points between times
    """
    args = request.args
    range = args.get('range')
    name = name if name else '*'

    print(range)

    if not (range):
        return "Please enter a valid total range", 400

    query = f'''
    from(bucket:"{settings.DB_NAME}")\
    |> range(start: -{range}d)\
    |> filter(fn:(r) => r._measurement=="user_skills")\
    |> filter(fn:(r) => r.name=="{name}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    # 
    result = query_api.query_data_frame(org=settings.ORG, query=query)

    fig = Figure(figsize=(10,10))
    axis = fig.add_subplot()
    # Add all skills
    for skill in settings.SKILLS:
        axis.plot(result["_time"], result[skill], label=skill)

    print(result["hitpoints"])

    x_labels = [time.strftime('%m/%d') for time in result["_time"]]
    axis.set_xticklabels(x_labels)
    
    axis.ticklabel_format(axis='y', style='plain')
    axis.set_title(f"{name}'s skills for the last")
    axis.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    FigureCanvas(fig).print_png(buf)
    return Response(buf.getvalue(), mimetype='image/png')

    return list(q_r)


if __name__ == "__main__":
    name()
