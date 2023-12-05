DROP DATABASE IF EXISTS LectureHalls;
CREATE DATABASE LectureHalls;

CREATE TABLE LectureHalls.Courses (
    courseID INTEGER NOT NULL,
    courseTitle VARCHAR(280) NOT NULL,
    location VARCHAR(50) NOT NULL,
    PRIMARY KEY(courseID)
);

/* ISO Strings are at most 27 characters long */
CREATE TABLE LectureHalls.Monday (
    courseID INTEGER NOT NULL PRIMARY KEY,
    time_start VARCHAR(27) NOT NULL,
    time_end VARCHAR(27) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
);

CREATE TABLE LectureHalls.Tuesday (
    courseID INTEGER NOT NULL PRIMARY KEY,
    time_start VARCHAR(27) NOT NULL,
    time_end VARCHAR(27) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
);

CREATE TABLE LectureHalls.Wednesday (
    courseID INTEGER NOT NULL PRIMARY KEY,
    time_start VARCHAR(27) NOT NULL,
    time_end VARCHAR(27) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
);

CREATE TABLE LectureHalls.Thursday (
    courseID INTEGER NOT NULL PRIMARY KEY,
    time_start VARCHAR(27) NOT NULL,
    time_end VARCHAR(27) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
);

CREATE TABLE LectureHalls.Friday (
    courseID INTEGER NOT NULL PRIMARY KEY,
    time_start VARCHAR(27) NOT NULL,
    time_end VARCHAR(27) NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE
);

