import json
import requests
import time
from timeentry import TimeEntry
import csv
import math

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
            #print('Row Found!')
            return row
        else:
            #print ('No Data Found')
            return None

    def printUploadList(self):
        for P in self.uploadList:
            print('Toggl Project:{} TogglID:{}\n'
                  'TD Project:{} TD ID:{}\n'
                  'Date:{} Duration:{}\n'.format(P.togglProject,
                                            P.togglID,
                                            P.tdProject,
                                            P.tdID,
                                            P.date,P.duration))

    def correctTimeFormat(self,time):
        pass

    def convertToMinutes(self,duration):
        minutes = round(duration * 60,0)
        return minutes

    def translate(self):
        found = 0
        notFound = 0
        for row in self.entryList:
            #print('Toggl Project to Look up:{}'.format(row.togglID))
            match = self.findMatchingProject(row.togglID)
            if match == None:
                notFound = notFound + 1
            else:
                found = found + 1
                self.uploadList.append(TimeEntry(row.date,self.convertToMinutes(row.duration),row.togglProject,match['td_project_name'],row.togglID,match['td_project_id']))
        print('{} rows Matched, {} rows not match'.format(found,notFound))

            

    





