from calendar import monthrange
from timeentry import TimeEntry
import requests
from requests.auth import HTTPBasicAuth
import json
import math

class TogglApi:
    def __init__(self,apiToken,apiBaseURL,userID,workspaceID,clientID,userAgent):
        self.apiToken = apiToken
        self.apiBaseURL = apiBaseURL
        self.userID = userID
        self.workspaceID = workspaceID
        self.clientID = clientID
        self.userAgent = userAgent
        self.startDate =''
        self.endDate = ''
        self.projectEntries = []

    #convert user input into correct string for Toggl API
    def FormatMonth(self,userMonth):
        month_string =''
        if int(userMonth) < 10:
            month_string = '{}{}'.format('0',userMonth)
        return month_string

    def FormatStartDate(self,userMonth,userYear):
        month_string = self.FormatMonth(userMonth)
        start_date_time = '{}-{}-{}'.format(userYear,month_string,'01')
        return start_date_time

    def FormatEndDate(self,userMonth,userYear):
        month_range = monthrange(int(userYear), int(userMonth))
        month_string = self.FormatMonth(userMonth)
        end_date_time = '{}-{}-{}'.format(userYear,month_string,month_range[1])
        return end_date_time

    def SetReportMonth(self,userMonth,userYear):
        self.startDate = self.FormatStartDate(userMonth,userYear)
        self.endDate = self.FormatEndDate(userMonth,userYear)

    def formatDuration(self,rawDur):
        x = float((rawDur/1000)/60/60)
        #print(x)
        x = round(x,2)
        #print (x)
        return x 

    def GetPageCount(self):
        headers = {'Content-Type':'application/json'}
        api_url = '{}?workspace_id={}&since={}&until={}&user_ids={}&client_ids={}&user_agent={}'.format(self.apiBaseURL,
                                                                                                        self.workspaceID,
                                                                                                        self.startDate,
                                                                                                        self.endDate,
                                                                                                        self.userID,
                                                                                                        self.clientID,
                                                                                                        self.userAgent)

        response = requests.get(api_url, auth = HTTPBasicAuth(self.apiToken,'api_token'), headers=headers)
        
        print ('\nHTTP Response code was: {}\n'.format(response.status_code))

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            return math.ceil(data['total_count']/50)
        else:
            return None

    def TogglQuery(self, page):
        headers = {'Content-Type':'application/json'}
        api_url = '{}?workspace_id={}&since={}&until={}&user_ids={}&client_ids={}&user_agent={}&page={}'.format(self.apiBaseURL,
                                                                                                        self.workspaceID,
                                                                                                        self.startDate,
                                                                                                        self.endDate,
                                                                                                        self.userID,
                                                                                                        self.clientID,
                                                                                                        self.userAgent,
                                                                                                        page)

        response = requests.get(api_url, auth = HTTPBasicAuth(self.apiToken,'api_token'), headers=headers)
        
        print ('\nHTTP Response code was: {}\n'.format(response.status_code))

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            return data
        else:
            return None
        pass



    def GetProjectData(self):
        pages = self.GetPageCount()
        i=1

        while i <= pages:
            data = self.TogglQuery(i)
            if data is not None:
                for entry in data['data']:
                    self.projectEntries.append(TimeEntry(entry['start'],
                                                         entry['project'],
                                                         self.formatDuration(entry['dur'])))
            else:
                print('Request Failed')
            i = i+1
        return self.projectEntries

