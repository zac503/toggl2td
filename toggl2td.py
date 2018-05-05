import json
import requests
from requests.auth import HTTPBasicAuth
from calendar import monthrange

user_config = {}

with open('config.txt','r') as f:
    for line in f:
        user_config[line.split('=')[0]] = line.split("=")[1].rstrip()


#Fields
user_agent_format = 'user_agent'
workspace_id_format = 'workspace_id'
user_id_format = 'user_ids'
client_id_format = 'client_ids'
month = input("Month to gather? (format as 'x' example '3' for March) ")
year = input("Which Year? (format as 'xxxx' example '2018') ")

#convert user input into correct string for Toggl API
month_range = monthrange(int(year), int(month))
month_string =''
if int(month) < 10:
    month_string = '{}{}'.format('0',month)

# print(month_string)

start_date_time = '{}-{}-{}'.format(year,month_string,'01')
end_date_time = '{}-{}-{}'.format(year,month_string,month_range[1])
print(start_date_time)
print(end_date_time)


headers = {'Content-Type':'application/json'}



def getData():

    api_url = '{}?workspace_id={}&since={}&until={}&user_ids={}&client_ids={}&user_agent={}'.format(user_config['api_base_url'],user_config['workspace_id'],start_date_time,end_date_time,user_config['user_id'],user_config['project_client_id'],user_config['user_agent'])

    print(api_url)

    response = requests.get(api_url, auth = HTTPBasicAuth(user_config['api_token'],'api_token'), headers=headers)
    
    print ('\nHTTP Response code was: {}\n'.format(response.status_code))

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


data = getData()



if data is not None:
    print("Here's your info: ")
    print(data['total_count'])
    for entry in data['data']:
        print('{} - {}'.format(entry['project'],(entry['dur']/1000)/60/60))

    
else:
    print('Request Failed')

