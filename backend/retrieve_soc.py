""" This file retrieves the schedule of classes."""
import string
from configparser import ConfigParser
from db_connection import Database_Querying
from time import sleep
from typing import List
import requests
from datetime import datetime, timedelta
from pprint import pprint

INIT_PATH = "init_files/request.ini"

class RetrieveSOC:

    def __init__(self):
        """ Initialize. Open the INI file."""
        self.config = ConfigParser()
        self.config.read(INIT_PATH)

        # Get global values
        self.time_wait = self.config.getfloat('GLOBAL', 'wait')
        self.url = self.config.get('GLOBAL', 'website')
        self.skip_if = self.config.get('GLOBAL', 'skip')
        self.term = 'FALL'
        self.year = datetime.now().year

        # Create database object so that we can add to it
        self.db = Database_Querying(self.config.get('GLOBAL', 'table_file'))

    @staticmethod
    def process_time(time: str) -> dict:
        """ Return the time as a start and end as ISO strings.
        Assumes in the format %h:%m(a/p)-%h:%m(a/p)"""
        two_times = time.split('-')  # Strip off any leading spaces and split into two times
        two_times[0] = two_times[0].strip()
        two_times[1] = two_times[1].strip()

        # Get the start and end times. Assume a/p at end of end string
        start = two_times[0]
        end, am_pm = two_times[1][:-1], two_times[1][-1]

        # Process end first. Assume a/p at end.
        end_tObj = datetime.strptime(end, "%H:%M")
        if am_pm == 'p':
            end_tObj += timedelta(hours=12)

        # Process start. If an 'a' at the end, we know its the morning. Else, we do not know.
        if start.endswith('a'):
            start_tObj = datetime.strptime(start[:-1], "%H:%M")
        else:  # Now, have to check if am_pm == 'p'
            start_tObj = datetime.strptime(start, "%H:%M")
            if am_pm == 'p':
                start_tObj += timedelta(hours=12)

        return {'time start': start_tObj.isoformat(), 'time end': end_tObj.isoformat()}

    @staticmethod
    def clean_string(s: str) -> List[str]:
        s = s.strip()
        return s.split('|')

    def call_API(self):
        """ Calls the PeterPortal API."""
        for char in string.ascii_lowercase:
            depts = self.config.get('DEPARTMENTS', char)
            depts = self.clean_string(depts)
            if len(depts):
                for dept in depts:  # Each department that starts with this letter
                    dept = dept.replace(" ", "%20")
                    response = requests.get(self.url + f"term={self.year}%20{self.term}&department={dept}")
                    self.store_result(response)
                    sleep(self.time_wait)


    def store_result(self, json_res: requests.Response) -> None:
        """ With a result, iterate through it and store data."""
        res = json_res.json()
        for i in range(len(res['schools'])): # Iterate through each school
            for j in range(len(res['schools'][i]['departments'])): # Iterate through each department
                for k in range(len(res['schools'][i]['departments'][j]['courses'])): # Iterate through each course listing
                    courseTitle = res['schools'][i]['departments'][j]['courses'][k]['courseTitle']
                    for l in range(len(res['schools'][i]['departments'][j]['courses'][k]['sections'])):  # Iterate through each section
                        courseID = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['sectionCode']
                        for m in range(len(res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'])):  # Iterate through each meeting
                            place = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'][m]['bldg']
                            days = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'][m]['days']
                            time = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'][m]['time']
                            if time != self.skip_if and place != self.skip_if:
                                time_d = self.process_time(time)
                                try:
                                    self.db.insert_row(courseID=courseID, courseTitle=courseTitle, location=place,
                                                   days=days, time_start=time_d['time start'], time_end=time_d['time end'])
                                    print(courseID)
                                except:
                                    raise Exception()

if __name__ == "__main__":
    r = RetrieveSOC()
    r.call_API()


