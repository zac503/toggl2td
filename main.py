import json
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
timeTranslator.translate()
#Test 3 - Translate Entries



#Test 4 - Load Entry to TeamDynamix
