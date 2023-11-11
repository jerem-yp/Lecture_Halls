""" This file retrieves the schedule of classes."""
import string
from configparser import ConfigParser
from db_connection import Database_Querying
from time import sleep
from typing import List
import requests
from datetime import datetime
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
        self.db = Database_Querying()

    @staticmethod
    def clean_string(s: str) -> List[str]:
        s = s.strip()
        return s.split('|')

    def call_API(self):
        """ Calls the PeterPortal API."""
        for char in string.ascii_lowercase:
            depts = self.config.get('DEPARTMENTS', char)
            depts = self.clean_string(depts)
            print(depts)
            if len(depts):
                for dept in depts:  # Each department that starts with this letter
                    dept = dept.replace(" ", "%20")
                    response = requests.get(self.url + f"term={self.year}%20{self.term}&department={dept}")
                    self.store_result(response)


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
                            days = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'][m]['bldg']
                            time = res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'][m]['time']
                            print(courseTitle, courseID, days, time)
                        raise Exception()


if __name__ == "__main__":
    r = RetrieveSOC()
    r.call_API()


