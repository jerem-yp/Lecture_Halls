import sqlite3
from pathlib import Path

DATABASE_PATH = "schedule.db"

""" Create databases."""
class Database_Querying:

    def __init__(self, filename: str):
        """ Initialize an object. Save a cursor to the object."""
        if not self.database_exists(filename):
            self.create_tables(filename)
        self.connection = sqlite3.connect(filename)

    @staticmethod
    def database_exists(filename):
        """ Check if file exists. Connect to it if exists, else"""
        return Path.exists(filename)


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
                    location TEXT NOT NULL
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

