import json
import requests
import time
from timeentry import TimeEntry
import csv

class TimeTranslator:
    def __init__(self):
        self.entryList = []
        self.translationMap = {}
        self.uploadList = []

    def loadTranslationFile(self, filename):
        with open(filename, mode='r') as csv_file:
            self.translationMap = list(csv.DictReader(csv_file))


    def addTogglEntry(self, entry):
        self.entryList.append(entry)

    def loadTogglEntries(self, entrylist):
        self.entryList = entrylist

    def printCurrentEntryList(self):
        for P in self.entryList:
            print('Date:{} - Project:{} - Duration:{} - ID:{}'.format(P.date,
                                            P.togglProject,
                                            P.duration,
                                            P.togglID))

    def printCurrentTranslationMap(self):
        for row in self.translationMap:
            print('{}:{} - {}:{}'.format(row["toggl_project_name"],
                                        row["toggl_project_id"],
                                        row["td_project_name"],
                                        row["td_project_id"])
            )
    
    def findMatchingProject(self, entryID):
        row =  next((item for item in self.translationMap if item["toggl_project_id"] == str(entryID)),None)
        if row != None:
            print('Row Found')
            print('Project ID {} for Toggl Project {} has the following match in Team Dynamix TD Name:{} - ID:{}\n'.format(row["toggl_project_name"],
                                                                                                                         row["toggl_project_id"],
                                                                                                                         row["td_project_name"],
                                                                                                                         row["td_project_id"]
            ))
        else:
            print ('No Data Found')


    def translate(self):
        for row in self.entryList:
            print('Toggl Project to Look up:{}'.format(row.togglID))
            self.findMatchingProject(row.togglID)                

            

    





