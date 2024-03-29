import json
from TogglApi import TogglApi
import requests
from requests.auth import HTTPBasicAuth
from calendar import monthrange

user_config = {}

with open('config.txt','r') as f:
    for line in f:
        user_config[line.split('=')[0]] = line.split("=")[1].rstrip()

toggl_API = TogglApi(user_config['api_token'],
                     user_config['api_base_url'],
                     user_config['user_id'],
                     user_config['workspace_id'],
                     user_config['project_client_id'],
                     user_config['user_agent'])



month = input("Month to gather? (format as 'x' example '3' for March) ")
year = input("Which Year? (format as 'xxxx' example '2018') ")

toggl_API.SetReportMonth(month,year)
pageCount = toggl_API.GetPageCount()
entryList = toggl_API.GetProjectData()

j = 0
for P in entryList:
    print('{} - {} - {} - {}'.format(P.date,P.togglProject,P.duration,P.togglID))
    j = j+1
print(j)



"""
#print(data)

if data is not None:
    print("Here's your info: ")
    print(data['total_count'])
    for entry in data['data']:
        print('{} - {} - {}'.format(
            entry['start'],
            entry['project'],
            formatDuration(entry['dur'])
            ))
else:
    print('Request Failed')

def formatDuration(rawDur):
    x = float((rawDur/1000)/60/60)
    print(x)
    x = round(x,2)
    print (x)
    return x 
"""