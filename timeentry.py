class TimeEntry:
    def __init__(self,date,duration,togglproject = 'default toggl', tdproject = 'default td' ):
        self.duration = duration
        self.date = date
        self.togglProject = togglproject
        self.tdProject = tdproject

