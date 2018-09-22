#!/usr/bin/python3
import sqlite3
dbname = "test"

def db_init():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS buildings
        (
        buildingID      TEXT PRIMARY KEY NOT NULL,
        buildingName    TEXT NOT NULL
        );''')
    c.execute('''CREATE TABLE IF NOT EXISTS courses
        (
        courseID      TEXT PRIMARY KEY NOT NULL,
        courseName    TEXT NOT NULL
        );''')
    conn.commit()
    conn.close()
    print("Buildings table created successfully")    


def add_to_db(buildingID, buildingName, roomID, roomName, 
            roomType, courseID, times, day, weeks):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS {0} 
        (
        buildingID      TEXT NOT NULL,
        roomID          TEXT NOT NULL,
        roomName        TEXT,
        roomType        TEXT,
        courseID        TEXT,
        time            INTEGER,
        week            INTEGER,
        day             INTEGER, 
        FOREIGN KEY(buildingID) REFERENCES buildings(buildingID)
        UNIQUE (time, day, week)
        );'''.format(buildingID)
    #create table
    c.execute(query) 
    query = '''INSERT OR IGNORE INTO buildings(buildingID, buildingName)
              VALUES(?,?) '''
    values = (buildingID, buildingName)
    c.execute(query, values)
    
    query = '''INSERT OR IGNORE INTO {0}(buildingID, roomID, roomName, roomType, courseID, time, day, week)
              VALUES(?,?,?,?,?,?,?,?)'''.format(buildingID)
    for week in weeks:
        for time in times:
            values = (buildingID, roomID, roomName, roomType, courseID, time, day, week)
            c.execute(query, values)

    conn.commit()
    conn.close()
    print("Adding completed successfully")

def add_courses(courseID, courseName):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    query = '''INSERT OR REPLACE INTO courses(courseID, courseName)
              VALUES(?,?) '''
    values = (courseID, courseName)
    c.execute(query, values)
    conn.commit()
    conn.close()


db_init()

add_to_db('B16', 'B16', 'LG03', 'LG03', 'Lecture', 'MTRN3020', 
[22, 23], 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]);

add_to_db('B16', 'B16', 'LG03', 'LG03', 'Lecture', 'MTRN3020', 
[22, 23], 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]);

add_to_db('J18', 'J18', '212', '212', 'Laboratory', 'MTRN3020', 
[24, 25, 26, 27, 28, 29], 5, [5,7,9] );

add_to_db('J18', 'J18', '212', '212', 'Laboratory', 'MTRN3020', 
[24, 25, 26, 27, 28, 29], 5, [5,7,9] );

add_to_db('J17', 'J17', '203', '203', 'Tutorial-Laboratory', 'MTRN3020', 
[20, 21], 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]);

add_to_db('J17', 'J17', '203', '203', 'Tutorial-Laboratory', 'MTRN3020', 
[20, 21], 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]);