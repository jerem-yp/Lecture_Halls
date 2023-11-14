import sqlite3
from pathlib import Path
from typing import Generator
import os

CONFIG_PATH = "init_files/request.ini"

""" Create databases."""
class Database_Querying:

    def __init__(self, filename):
        """ Initialize an object. Save a cursor to the object."""
        try: # If there is an error raised, or interruption, the file isn't even created.
            self.turn_on_foreign_keys(filename)
        except Exception as e:
            os.remove(filename)
            print(e)
            exit()

        if not self.database_exists(filename):
            try:  # Similarly if an error is raised/interruption, the file isn't even created.
                self._create_tables(filename)
            except Exception as e:
                os.remove(filename)
                print(e)
                exit()

        self.filename = filename

    @staticmethod
    def database_exists(filename: str):
        """ Check if Courses table exists. Only """
        con = sqlite3.connect(filename)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = cur.fetchall()
        return len(res) > 0  # Were any tables found?

    @staticmethod
    def turn_on_foreign_keys(filename: str):
        """ Turn on foreign key constraints."""
        con = sqlite3.connect(filename)
        con.execute('PRAGMA foreign_keys = ON;')
        con.commit()
        con.close()


    @staticmethod
    def _create_tables(filename):
        """ SQLITE code for creating the tables."""
        con = sqlite3.connect(filename, isolation_level = None)
        cur = con.cursor()

        try:

            # First create table for all places
            cur.execute("""
                        CREATE TABLE Courses(
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
                        courseID INTEGER NOT NULL PRIMARY KEY,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
                        );"""
                        )

            cur.execute("""
                        CREATE TABLE Tuesday(
                        courseID INTEGER NOT NULL PRIMARY KEY,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
                        );""")

            cur.execute("""
                        CREATE TABLE Wednesday(
                        courseID INTEGER NOT NULL PRIMARY KEY,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
                        );""")

            cur.execute("""
                        CREATE TABLE Thursday(
                        courseID INTEGER NOT NULL PRIMARY KEY,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
                        );""")

            cur.execute("""
                        CREATE TABLE Friday(
                        courseID INTEGER NOT NULL PRIMARY KEY,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
                        );""")
        except Exception as e:
            cur.close()
            con.close()
            print(e)
            exit()

        con.commit()
        cur.close()
        con.close()

    # Add rows
    def insert_row(self, *, courseID: int, courseTitle: str, location: str, days: str, time_start: str, time_end: str) -> None:
        """ This function takes data from the classes and adds it to the database."""
        # First, check if the course is already inside. If it is, no addition to be made.
        if not self.row_already_exists(courseID=courseID):
            con = sqlite3.connect(self.filename)
            cur = con.cursor()
            data_tuple = (courseID, courseTitle, location)
            cur.execute("""
                        INSERT INTO Courses (courseID, courseTitle, location)
                        VALUES (?, ?, ?);
                        """, data_tuple)
            self._insert_into_tables(cur=cur, courseID=courseID, days=days, time_start=time_start, time_end=time_end)

            # Close
            cur.close()
            con.commit()
            con.close()




    def _insert_into_tables(self, *, cur: sqlite3.Cursor, courseID: int, days: str, time_start: str, time_end: str) -> None:
        """ This function takes time data and inserts into any tables."""
        data_tuple = {'courseID': courseID, 'time_start': time_start, 'time_end': time_end}

        if 'M' in days:  # Insert into Monday table
            cur.execute("""
                        INSERT INTO Monday (courseID, time_start, time_end)
                        VALUES (:courseID, :time_start, :time_end);""", data_tuple)

        if 'Tu' in days: # Insert into Tuesday table
            cur.execute("""
                        INSERT INTO Tuesday (courseID, time_start, time_end)
                        VALUES (:courseID, :time_start, :time_end);""", data_tuple)

        if 'W' in days:  # Insert into Wednesday table
            cur.execute("""
                        INSERT INTO Wednesday (courseID, time_start, time_end)
                        VALUES (:courseID, :time_start, :time_end);""", data_tuple)

        if 'Th' in days:  # Insert into Thursday table
            cur.execute("""
                        INSERT INTO Thursday (courseID, time_start, time_end)
                        VALUES (:courseID, :time_start, :time_end);""", data_tuple)

        if 'F' in days:  # Insert into Friday table
            cur.execute("""
                        INSERT INTO Friday (courseID, time_start, time_end)
                        VALUES (:courseID, :time_start, :time_end);""", data_tuple)

    # Check if course is already in DB.
    def row_already_exists(self, *, courseID: int) -> bool:
        """ Check if the courseID already exists. """
        # Get connection
        con = sqlite3.connect(self.filename)
        cur = con.cursor()

        placeholder = (courseID, )
        cur.execute(f"""
                    SELECT courseID
                    FROM Courses
                    WHERE courseID = ?
                    ;""", placeholder)
        res = cur.fetchall()

        # Close connection
        cur.close()
        con.close()

        return len(res) > 0

    # Queries to get data from this DB
    def get_all_for_day(self, day: str):
        """ Given a day (Monday, Tuesday, Wednesday, Thursday, Friday), find all classes and times on that day."""
        # Get connection
        con = sqlite3.connect()
        cur = con.cursor()

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

        cur.close()
        con.close()

    def get_all_for_class(self, day: str, cls_name: str):
        """ For a single classroom, get all results."""
        """ Given a day (Monday, Tuesday, Wednesday, Thursday, Friday), find all classes and times on that day."""
        # Get connection
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        loc = {'location': cls_name}
        if day == 'Monday':
            cur.execute("""
                        SELECT Courses.courseID, Courses.location, Monday.time_start, Monday.time_end
                        FROM Courses
                        INNER JOIN Monday on Monday.courseID = Courses.courseID
                        WHERE Courses.location = :location;
                        """, loc)

        elif day == 'Tuesday':
            cur.execute("""
                        SELECT Courses.courseID, Courses.location, Tuesday.time_start, Tuesday.time_end
                        FROM Courses
                        INNER JOIN Tuesday on Tuesday.courseID = Courses.courseID
                        WHERE Courses.location = :location;
                        """, loc)

        elif day == 'Wednesday':
            cur.execute("""
                        SELECT Courses.courseID, Courses.location, Wednesday.time_start, Wednesday.time_end
                        FROM Courses
                        INNER JOIN Wednesday on Wednesday.courseID = Courses.courseID
                        WHERE Courses.location = :location;
                        """, loc)

        elif day == 'Thursday':
            cur.execute("""
                        SELECT Courses.courseID, Courses.location, Thursday.time_start, Thursday.time_end
                        FROM Courses
                        INNER JOIN Thursday on Thursday.courseID = Courses.courseID
                        WHERE Courses.location = :location;
                        """, loc)

        elif day == 'Friday':
            cur.execute("""
                        SELECT Courses.courseID, Courses.location, Friday.time_start, Friday.time_end
                        FROM Courses
                        INNER JOIN Friday on Friday.courseID = Courses.courseID
                        WHERE Courses.location = :location;
                        """, loc)

        else:
            raise Exception("Day is invalid.")

        res = cur.fetchone()
        while res:
            yield res
            res = cur.fetchone()

        # Close database
        cur.close()
        con.close()

    def clear_database(self) -> None:
        """ DELETES EVERY ROW from table"""
        # Get connection
        con = sqlite3.connect(self.filename)
        cur = con.cursor()

        cur.execute("""
                    DELETE FROM Courses;
                    """)

        # Commit and close
        con.commit()
        cur.close()
        con.close()