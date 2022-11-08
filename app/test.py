from datetime import datetime

"""from influxdb import InfluxDBClient
#from rich import print

client = InfluxDBClient('localhost', 8086)
client.create_database('testdb2')
client.switch_database('testdb2')

json_payload = [
]

for i in range(1, 7):
    json_payload.append(
        {
            "measurement": "activity",
            "tags": {
                "name": "Gandalf"
            },
            "time": i,
            "fields": {
                "steps": i * 500,
                "miles": i//2
            }
        }
    )
"""

print("Hello")

date = datetime.now().ctime()

print("Scraping at " +  date)

#client.write_points(json_payload, database="testdb2")

#uery_result = client.query('select * from activity;')
#gandalf_points = query_result.get_points(tags={"name": "Gandalf"})

#print(query_result)
#print(list(gandalf_points))
#print(client.query('select * from activity;'))

"""
[
    {
        "measurement": "activity",
        "tags": {
            "name": "Gandalf"
        },
        "time": 4,
        "fields": {
            "steps": 6000,
            "miles": 3
        }
    },
    {
        "measurement": "activity",
        "tags": {
            "name": "Gandalf"
        },
        "time": 5,
        "fields": {
            "steps": 8000,
            "miles": 4
        }
    },
    {
        "measurement": "activity",
        "tags": {
            "name": "Gandalf"
        },
        "time": 6,
        "fields": {
            "steps": 10000,
            "miles": 5
        }
    },
]

"""
