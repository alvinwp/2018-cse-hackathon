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
        courseID      TEXT PRIMARY KEY NOT NULL,
        courseName    TEXT NOT NULL
        );''')
    conn.commit()
    conn.close()
    print("Buildings table created successfully")    


def add_to_db(buildingID, buildingName, roomID, roomName, 
            roomType, times, days, weeks):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS {0} 
        (
        FOREIGN KEY(buildingID) REFERENCES buildings(buildingID)
        roomID          TEXT NOT NULL,
        roomName        TEXT,
        roomType        TEXT,
        time            INTEGER,
        week            INTEGER,
        day             INTEGER
        );'''.format(buildingID)
    #create table
    c.execute(query) 
    query = '''INSERT OR IGNORE INTO buildings(buildingID, buildingName)
              VALUES(?,?) '''
    values = (buildingID, buildingName)
    c.execute(query, values)
    
    query = '''INSERT INTO {0}(roomID, roomName, roomType, time, day, week)
              VALUES(?,?,?,?,?,?)'''.format(buildingID)
    for week in weeks:
        for time in time:
            values = (roomID, roomName, roomType, time, day, week)
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