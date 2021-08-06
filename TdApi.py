import json
import requests
import time

class TdApi:
    def __init__(self,beid,key):
        self.beid = beid
        self.key = key
        self.token = ''
        self.user_id = ''
        self.client_id = ''
        self.user_dict = []


    def add_time(self):
        pass

    def authenticate(self):
        response = requests.post('https://wcu.teamdynamix.com/TDWebApi/api/auth/loginadmin', data={
            'BEID':self.beid,
            'WebServicesKey':self.key})
        #print('Authenticate Response:{0}'.format(response))
        self.token = response.text
        if response.status_code == 200:
            print('Authentication Successful')
        else:
            print('Authentication Failed')

    def get_time (self,session):
        ###requests.get('https://wcu.teamdynamix.com/TDWebApi/api/time/report/{reportDate}/{uid}'.format())
        pass

    def get_user(self,user):
        response = requests.get('https://wcu.teamdynamix.com/TDWebApi/api/people/lookup?searchText={searchText}&maxResults={maxResults}'.format(searchText = user,maxResults = '1'), headers={'Authorization':'Bearer {0}'.format(self.token)})
        #print('Get User Response:{0}'.format(response))
        #print(response.text)
        self.user_dict = json.loads(response.text)
        return self.user_dict[0]['UID']

    def set_default_user(self,uid):
        self.user_id = uid

    def get_project_list(self, user = 'default'):
        if user == 'default':
            user = self.user_id
        response = requests.post('https://wcu.teamdynamix.com/TDWebApi/api/projects/search',
            headers={
                     'Authorization':'Bearer {0}'.format(self.token),
                     'Content-Type':'text/json'},
                    json={'AccountIDs': [self.user_id]})
        print('Get Projects Response:{0}'.format(response))
        project_dict = json.loads(response.text)
        return project_dict

    def add_time_entry(self,entry):
        response = requests.post('https://api.teamdynamix.com/TDWebApi/api/time',
                                headers={'Authorization':'Bearer {0}'.format(self.token),
                                        'Content-Type':'text/json'},
                                json=entry)
        print('Add Time Entry Response:{0}'.format(response.content))    
        
    def get_time_types(self):
        response = requests.get('https://api.teamdynamix.com/TDWebApi/api/time/types',
                                headers={'Authorization':'Bearer {0}'.format(self.token),
                                        'Content-Type':'text/json'})
        timeTypes = json.loads(response.text)
        return timeTypes

    def get_applications(self):
        response = requests.get('https://api.teamdynamix.com/TDWebApi/api/applications',
                                headers={'Authorization':'Bearer {0}'.format(self.token),
                                        'Content-Type':'text/json'})
        applications = json.loads(response.text)
        return applications

    def write_project_file(self,project_list):
        filename = '{}-{}.txt'.format(self.user_id[0:7],time.time())
        
        try:
            file = open(filename,'a')
            for item in project_list:
                file.write('{}|{}\n'.format(item['Name'],item['ID']))
            file.close()
            print('File {} written successfully'.format(filename))
        except:
            print('File Creation Failed')

        



# session_token = authenticate()
# user_id = getUser('Zach Phillips',session_token)
# #print(user_id)
# #project_search = {'AccountIDs': [user_id]}
# #getProjectList(project_search,session_token)
# timeEntry = [{'TimeID':'0',
#               'Uid':user_id,
#               'TimeTypeID':'2448',
#               'Component':'1',
#               'Minutes':'60',
#               'ProjectID':'401570',
#               'TimeDate':'2021-07-20T00:00:00-05:00' }]

# addTimeEntry(timeEntry,session_token)

# timeTypes = getTimeTypes(session_token)
# applications = getApplications(session_token)

# for type in timeTypes:
#     print('{} - {}'.format(type['ID'],type['Name']))

# for app in applications:
#     print('{} - {}'.format(app['AppID'],app['Name']))