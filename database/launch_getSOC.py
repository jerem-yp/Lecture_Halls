""" This file retrieves the schedule of classes."""
import string
from configparser import ConfigParser
from time import sleep
import requests
from datetime import datetime, timedelta
import mysql.connector
import sys
from pprint import pprint

from typing import List

INIT_PATH = "init/user.ini"

class RetrieveSOC:

    def __init__(self):
        """ Initialize. Open the INI file."""
        self.config = ConfigParser()
        self.config.read(INIT_PATH)

        # Get api data
        self.time_wait = self.config.getfloat('API', 'wait')
        self.url = self.config.get('API', 'url')
        self.skip_if = self.config.get('API', 'skip')
        self.term = self.config.get('API', 'season')
        self.year = datetime.now().year

        # Get login credentials
        self.host = self.config.get('LOGIN', 'host')
        self.user = self.config.get('LOGIN', 'user')
        self.database = self.config.get('LOGIN', 'database')
        self.password = input('Password: ')

        # Clear database of data
        self.clear_database()

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

    @staticmethod
    def get_building_room(place_name: str):
        """ From a room (i.e. ALP 1000) get the building (ALP) and room number (1000)"""
        place = place_name.split()
        building = " ".join(place[:-1]) # Numbers are the last element
        room = place[-1]
        return building, room

    def call_API(self):
        """ Calls the PeterPortal API."""
        for char in string.ascii_lowercase:
            depts = self.config.get('DEPARTMENTS', char)
            depts = self.clean_string(depts)
            if len(depts):
                for dept in depts:  # Each department that starts with this letter
                    dept = dept.replace(" ", "%20")
                    response = requests.get(self.url + f"term={self.year}%20{self.term}&department={dept}")
                    if 'message' in response and response['message'] == 'Internal Server Error':
                        print(dept)
                    else:
                        self.store_result(response)
                        sleep(self.time_wait)


    def store_result(self, json_res: requests.Response) -> None:
        """ With a result, iterate through it and store data."""
        res = json_res.json()
        try:
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
                                    building, room = self.get_building_room(place)
                                    try:
                                        self.insert_row(courseID=courseID, courseTitle=courseTitle, location=building, room=room,
                                                       days=days, time_start=time_d['time start'], time_end=time_d['time end'])
                                        print(courseID)
                                    except:
                                        pprint(res['schools'][i]['departments'][j]['courses'][k]['sections'][l]['meetings'])
                                        raise Exception()
        except KeyError as k:
            print(k)
            pprint(res)
            sys.exit()


    def insert_row(self, *, courseID: int, courseTitle: str, location: str, days: str, room:str, time_start: str, time_end: str):
        """ Insert a single row into the database. Write to """
        in_courses = self.check_course_exists(courseID)

        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as err:  # STOP the code
            print("Error while connecting to MySQL: ", err)
            sys.exit()

        cursor = connection.cursor()

        if not in_courses:
            # First, write to the 'courses' table
            insert_query = """INSERT INTO Courses (courseID, courseTitle, location, room) VALUES (%s, %s, %s, %s)"""
            insert_values = (courseID, courseTitle, location, room)
            cursor.execute(insert_query, insert_values)

        if 'M' in days:
            insert_query = """INSERT INTO Monday (courseID, time_start, time_end) VALUES (%s, %s, %s)"""
            insert_values = (courseID, time_start, time_end)
            cursor.execute(insert_query, insert_values)

        if 'Tu' in days:
            insert_query = """INSERT INTO Tuesday (courseID, time_start, time_end) VALUES (%s, %s, %s)"""
            insert_values = (courseID, time_start, time_end)
            cursor.execute(insert_query, insert_values)

        if 'W' in days:
            insert_query = """INSERT INTO Wednesday (courseID, time_start, time_end) VALUES (%s, %s, %s)"""
            insert_values = (courseID, time_start, time_end)
            cursor.execute(insert_query, insert_values)

        if 'Th' in days:
            insert_query = """INSERT INTO Thursday (courseID, time_start, time_end) VALUES (%s, %s, %s)"""
            insert_values = (courseID, time_start, time_end)
            cursor.execute(insert_query, insert_values)

        if 'F' in days:
            insert_query = """INSERT INTO Friday (courseID, time_start, time_end) VALUES (%s, %s, %s)"""
            insert_values = (courseID, time_start, time_end)
            cursor.execute(insert_query, insert_values)

        if connection.is_connected():
            connection.commit()
            connection.close()

    def check_course_exists(self, courseID: int) -> bool:
        """ Check if a class is already in the database. Don't store if not."""
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as err:  # STOP the code
            print("Error while connecting to MySQL: ", err)
            sys.exit()

        cursor = connection.cursor()
        query = """SELECT courseID FROM Courses WHERE courseID=(%s)"""
        data = (courseID,)
        cursor.execute(query, data)
        in_database = len(cursor.fetchall()) > 0

        if connection.is_connected():
            connection.close()

        return in_database

    def clear_database(self):
        """ Clear all tables. There is a 'DELETE CASCADE', which is all that needs to be deleted is the
        Courses table."""
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as err:  # STOP the code
            print("Error while connecting to MySQL: ", err)
            sys.exit()

        try:
            cursor = connection.cursor()
            delete_query = """DELETE FROM Courses"""
            cursor.execute(delete_query)
        except mysql.connector.Error as err:  # STOP the code
            print("Error while connecting to MySQL: ", err)
            sys.exit()
        finally:
            if connection.is_connected():
                connection.commit()
                connection.close()

def main():
    database = RetrieveSOC()
    database.call_API()  # Process it


if __name__ == "__main__":
    main()

