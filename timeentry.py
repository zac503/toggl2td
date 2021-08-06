class TimeEntry:
    def __init__(self,date,duration,togglproject = 'default toggl', tdproject = 'default td', togglID = 'NULL', tdID = 'Null' ):
        self.duration = duration
        self.date = date
        self.togglProject = togglproject
        self.tdProject = tdproject
        self.togglID = togglID
        self.tdID = tdID

