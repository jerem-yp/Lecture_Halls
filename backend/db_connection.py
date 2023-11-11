import sqlite3
from pathlib import Path
from typing import Generator
DATABASE_PATH = "schedule.db"

""" Create databases."""
class Database_Querying:

    def __init__(self, filename: str = 'classes.db'):
        """ Initialize an object. Save a cursor to the object."""
        if not self.database_exists(filename):
            self.create_tables(filename)
        self.connection = sqlite3.connect(filename)

    @staticmethod
    def database_exists(filename: str):
        """ Check if file exists. Connect to it if exists, else"""
        return Path.exists(Path(filename))


    @staticmethod
    def create_tables(filename):
        """ SQLITE code for creating the tables."""
        con = sqlite3.connect(filename)
        cur = con.cursor()

        # First create table for all places
        cur.execute("""
                    CREATE TABLE courses(
                    courseID INTEGER NOT NULL,
                    courseTitle TEXT NOT NULL,
                    location TEXT NOT NULL,
                    PRIMARY KEY(courseID)
                    );"""
                    )
        # Now create table for each day of the week, M-F
        # These data structures make it easier to get data for each day
        cur.execute("""
                    CREATE TABLE Monday(
                    courseID INTEGER NOT NULL
                    time_start TEXT NOT NULL
                    time_end TEXT NOT NULL
                    PRIMARY KEY(courseID)
                    FOREIGN KEY (courseID) REEFERENCES Courses(courseID)
                    );""")

        cur.execute("""
                    CREATE TABLE Tuesday(
                    courseID INTEGER NOT NULL
                    time_start TEXT NOT NULL
                    time_end TEXT NOT NULL
                    PRIMARY KEY(courseID)
                    FOREIGN KEY (courseID) REEFERENCES Courses(courseID)
                    );""")

        cur.execute("""
                    CREATE TABLE Wednesday(
                    courseID INTEGER NOT NULL
                    time_start TEXT NOT NULL
                    time_end TEXT NOT NULL
                    PRIMARY KEY(courseID)
                    FOREIGN KEY (courseID) REEFERENCES Courses(courseID)
                    );""")

        cur.execute("""
                    CREATE TABLE Thursday(
                    courseID INTEGER NOT NULL
                    time_start TEXT NOT NULL
                    time_end TEXT NOT NULL
                    PRIMARY KEY(courseID)
                    FOREIGN KEY (courseID) REEFERENCES Courses(courseID)
                    );""")

        cur.execute("""
                    CREATE TABLE Friday(
                    courseID INTEGER NOT NULL
                    time_start TEXT NOT NULL
                    time_end TEXT NOT NULL
                    PRIMARY KEY(courseID)
                    FOREIGN KEY (courseID) REEFERENCES Courses(courseID)
                    );""")

    # Add rows
    def insert_row(self, *, courseID: int, courseTitle: str, location: str, days: str, time_start: str, time_end: str) -> None:
        """ This function takes data from the classes and adds it to the database."""
        # First, check if the course is already inside. If it is, no addition to be made.
        if not self.row_already_exists(courseID=courseID):
            cur = self.connection.cursor()
            data_tuple = (courseID, courseTitle, location)
            cur.execute("""
                        INSERT INTO Courses 
                        VALUES (?, ?, ?);
                        """, data_tuple)
            self._insert_into_tables(courseID=courseID, days=days, time_start=time_start, time_end=time_end)



    def _insert_into_tables(self, *, courseID: int, days: str, time_start: str, time_end: str) -> None:
        """ This function takes time data and inserts into any tables."""
        data_tuple = (courseID, time_start, time_end)
        cur = self.connection.cursor()
        if 'M' in days:  # Insert into Monday table
            cur.execute("""
                        INSERT INTO Monday
                        VALUES (?, ?, ?);""", data_tuple)

        if 'Tu' in days: # Insert into Tuesday table
            cur.execute("""
                        INSERT INTO Tuesday
                        VALUES (?, ?, ?);""", data_tuple)

        if 'W' in days:  # Insert into Wednesday table
            cur.execute("""
                        INSERT INTO Wednesday
                        VALUES (?, ?, ?);""", data_tuple)

        if 'Th' in days:  # Insert into Thursday table
            cur.execute("""
                        INSERT INTO Thursday
                        VALUES (?, ?, ?);""", data_tuple)

        if 'F' in days:  # Insert into Friday table
            cur.execute("""
                        INSERT INTO Monday
                        VALUES (?, ?, ?);""", data_tuple)

    # Check if course is already in DB.
    def row_already_exists(self, *, courseID: int) -> bool:
        """ Check if the courseID already exists. """
        cur = self.connection.cursor()
        placeholder = (courseID, )
        cur.execute(f"""
                    SELECT courseID
                    FROM Courses
                    WHERE courseID = ?
                    );""", placeholder)
        res = cur.fetchall()
        return len(res) > 0

    # Queries to get data from this DB
    def get_all_for_day(self, day: str):
        """ Given a day (Monday, Tuesday, Wednesday, Thursday, Friday), find all classes and times on that day."""
        cur = self.connection.cursor()
        if day == 'Monday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Monday on Monday.courseID = Courses.courseID
                        );""")

        elif day == 'Tuesday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Tuesday on Tuesday.courseID = Courses.courseID
                        );""")

        elif day == 'Wednesday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Wednesday on Wednesday.courseID = Courses.courseID
                        );""")

        elif day == 'Thursday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Thursday on Thursday.courseID = Courses.courseID
                        );""")

        elif day == 'Friday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Friday on Friday.courseID = Courses.courseID
                        );""")

        else:
            raise Exception("Day is invalid.")

        res = cur.fetchone()
        while res:
            yield res
            res = cur.fetchone()

    def get_all_for_class(self, day: str, cls_name: str):
        """ For a single classroom, get all results."""
        """ Given a day (Monday, Tuesday, Wednesday, Thursday, Friday), find all classes and times on that day."""
        cur = self.connection.cursor()
        loc = (cls_name, )
        if day == 'Monday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Monday on Monday.courseID = Courses.courseID
                        WHERE Courses.location = ?
                        );""", loc)

        elif day == 'Tuesday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Tuesday ON Tuesday.courseID = Courses.courseID
                        WHERE Courses.location = ?
                        );""", loc)

        elif day == 'Wednesday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Wednesday on Wednesday.courseID = Courses.courseID
                        WHERE Courses.location = ?
                        );""", loc)

        elif day == 'Thursday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Thursday on Thursday.courseID = Courses.courseID
                        WHERE Courses.location = ?
                        );""", loc)

        elif day == 'Friday':
            cur.execute("""
                        SELECT courseID, location, time_start, time_end
                        FROM Courses
                        INNER JOIN Friday on Friday.courseID = Courses.courseID
                        WHERE Courses.location = ?
                        );""", loc)

        else:
            raise Exception("Day is invalid.")

        res = cur.fetchone()
        while res:
            yield res
            res = cur.fetchone()