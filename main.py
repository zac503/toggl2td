import json
from timeentry import TimeEntry
from TogglApi import TogglApi
from TdApi import TdApi
import requests
from requests.auth import HTTPBasicAuth
from calendar import monthrange
import csv
from Translator import TimeTranslator

#Setup the mapping file and load into memory
translationFile = 'projDB.csv'
timeTranslator = TimeTranslator()
timeTranslator.loadTranslationFile(translationFile)

#Load User Configuration
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

td_API = TdApi(user_config['td_api_BEID'],
               user_config['td_api_Key']
)


#Test 1 - Pull Toggl Entries - WORKING

month = input("Month to gather? (format as 'x' example '3' for March) ")
year = input("Which Year? (format as 'xxxx' example '2018') ")

toggl_API.SetReportMonth(month,year)
pageCount = toggl_API.GetPageCount()
entryList = toggl_API.GetProjectData()

#Test 2 - Load Entries into Translator - WORKING


timeTranslator.loadTogglEntries(entryList)
#timeTranslator.printCurrentEntryList()
#timeTranslator.printCurrentTranslationMap()

#Test 3 - Translate Entries
timeTranslator.translate()
timeTranslator.printUploadList()


#Test 4 - Load Entry to TeamDynamix

td_API.authenticate()
user_id = td_API.get_user('Zach Phillips')
td_API.set_default_user(user_id)
for entry in timeTranslator.uploadList:
    timeEntry = td_API.create_time_entry(entry)
    print(timeEntry)
    confirm = input("\nDo you want to upload the above entry? (y/n)")
    if confirm == 'y':
        td_API.add_time_entry(timeEntry)
