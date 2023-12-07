import mysql.connector
import configparser
from pathlib import Path
import sys

# Get path. Only works if in cwd
CONFIG_PATH = Path.cwd() / "init/request.ini" if str(Path.cwd()).endswith('backend') else Path.cwd() / "backend/init/request.ini"

""" Create databases."""
class Database_Querying:

    def __init__(self):
        config = configparser.ConfigParser()

        try:  # If no config error, stop
            config.read(CONFIG_PATH)
        except FileNotFoundError:
            print('INI File does not exist.')

        self.host = config.get('LOGIN', 'host')
        self.user = config.get('LOGIN', 'username')
        self.password = config.get('LOGIN', 'password')
        self.database = config.get('LOGIN', 'database')

    def get_single_room(self, building: str, room: str, day: str):
        """ Given a building and a room, query the database. """
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as E:
            raise Exception('Connection error: ', E)

        cursor = connection.cursor()

        if day == 'M':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s AND C.room = %s) AS c                       
                    INNER JOIN Monday AS day ON c.courseID = day.courseID;"""
            data = (building, room)
            cursor.execute(query, data)

        elif day == 'Tu':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s AND C.room = %s) AS c                       
                    INNER JOIN Tuesday AS day ON c.courseID = day.courseID;"""
            data = (building, room)
            cursor.execute(query, data)

        elif day == 'W':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s AND C.room = %s) AS c                       
                    INNER JOIN Wednesday AS day ON c.courseID = day.courseID;"""
            data = (building, room)
            cursor.execute(query, data)

        elif day == 'Th':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s AND C.room = %s) AS c                       
                    INNER JOIN Thursday AS day ON c.courseID = day.courseID;"""
            data = (building, room)
            cursor.execute(query, data)

        elif day == 'F':

            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s AND C.room = %s) AS c                       
                    INNER JOIN Friday AS day ON c.courseID = day.courseID;"""
            data = (building, room)
            cursor.execute(query, data)

        else:
            raise Exception('Day does not exist.')

        courses = cursor.fetchall()

        if connection.is_connected():
            connection.close()

        return courses


    def get_building(self, building: str, day: str):
        """ Given a building, query the database.  And get all classes in that building. """
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as E:
            raise Exception('Connection error: ', E)

        cursor = connection.cursor()

        if day == 'M':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s) AS c                       
                    INNER JOIN Monday AS day ON c.courseID = day.courseID;"""
            data = (building,)
            cursor.execute(query, data)

        elif day == 'Tu':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s) AS c                       
                    INNER JOIN Tuesday AS day ON c.courseID = day.courseID;"""
            data = (building,)
            cursor.execute(query, data)

        elif day == 'W':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s) AS c                       
                    INNER JOIN Wednesday AS day ON c.courseID = day.courseID;"""
            data = (building,)
            cursor.execute(query, data)

        elif day == 'Th':
            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s) AS c                       
                    INNER JOIN Thursday AS day ON c.courseID = day.courseID;"""
            data = (building,)
            cursor.execute(query, data)

        elif day == 'F':

            query = """
                    SELECT c.courseTitle, day.time_start, day.time_end
                    FROM (SELECT *
                          FROM Courses AS C
                          WHERE C.location = %s) AS c                       
                    INNER JOIN Friday AS day ON c.courseID = day.courseID;"""
            data = (building,)
            cursor.execute(query, data)

        else:
            raise Exception('Day does not exist.')

        courses = cursor.fetchall()

        if connection.is_connected():
            connection.close()

        return courses

    def get_all_classrooms(self):
        """ Get all classrooms where classes are taking place on campus."""
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as E:
            raise Exception('Connection error: ', E)

        cursor = connection.cursor()
        query = """SELECT DISTINCT location, room FROM Courses"""
        cursor.execute(query)
        rooms = cursor.fetchall()

        if connection.is_connected():
            connection.close()

        return rooms

    def get_all_buildings(self):
        """ Get all the buildings in the school where classes are taking place."""
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.connector.Error as E:
            raise Exception('Connection error: ', E)

        cursor = connection.cursor()
        query = """SELECT DISTINCT location FROM Courses"""
        cursor.execute(query)
        buildings = cursor.fetchall()

        if connection.is_connected():
            connection.close()

        return buildings


if __name__ == "__main__":
    db = Database_Querying()
    #db.get_single_room('EH', '1200', 'Th')
    #db.get_all_classrooms()
    #db.get_all_buildings()
    #db.get_building('EH', 'Th') \
    # print(db.get_building('EH', 'Th'))
    # print(db.get_single_room('EH', '1200','Th'))