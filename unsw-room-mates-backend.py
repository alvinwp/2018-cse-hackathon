#!/usr/bin/python3
import sqlite3
from time import gmtime, strftime

DBNAME = "db/unsw_roommate"

def get_all_building_names():

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # Get the data
    query = c.execute('''SELECT buildingName
                         FROM buildings''')

    # Return it
    data = [row[0] for row in query]
    conn.close()
    return data
    

def get_all_building_ids():

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # Get the data
    query = c.execute('''SELECT buildingID
                         FROM buildings''')

    # Return it
    data = [row[0] for row in query]
    conn.close()
    return data


def get_all_buildings_mapping():

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # Get the data
    query = c.execute('''SELECT buildingName, buildingID
                         FROM buildings''')
    if query == None:
        conn.close()
        return None

    # Return it
    data = {i: j for (i, j) in query}
    conn.close()
    return data

def get_all_building_mappings_parsed():
    buildings = get_all_buildings_mapping()
    if buildings == None:
        return None

    return [[i, buildings[i]] for i in buildings]

def get_room_from_day_week(buildingID, roomID, day, week):

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get the data
    try:
        c.execute('''SELECT *
                            FROM {0}
                            WHERE roomID=? AND
                                  day=? AND
                                  week=?'''.format(buildingID), (roomID,day,week,))
    except sqlite3.OperationalError:
        conn.close()
        return None

    # Get only the time
    result = [dict(row) for row in c.fetchall()]
    times = [row["time"] for row in result]

    conn.close()
    return times

def get_rooms_from_building(buildingID, day, week):

    # Get the rooms in the building
    building_rooms = {}

    room_ids = get_all_room_ids(buildingID)

    if room_ids == None:
        return None
    
    for roomID in room_ids:
        building_rooms[roomID] = get_room_from_day_week(buildingID, roomID, day, week)

    return building_rooms

def get_free_rooms_from_building(buildingID, time_int, day, week):
    building_rooms = get_rooms_from_building(buildingID, day, week)
    if building_rooms == None:
        return None

    free_rooms = []

    for room in building_rooms:
        if time_int not in building_rooms[room]:
            free_rooms.append(room)

    return free_rooms

def get_buildings_free(time_int, day, week):
    
    # Get all the building ids
    building_ids = get_all_building_ids()
    if building_ids == None:
        return None

    n_free_rooms = {}
    for building in building_ids:
        n_free_rooms[building] = len(get_free_rooms_from_building(building, time_int, day, week))

    sorted_n_free_rooms = []

    for k, v in [(k, n_free_rooms[k]) for k in sorted(n_free_rooms, key=n_free_rooms.get, reverse=True)]:
        sorted_n_free_rooms.append([k, v])

    return sorted_n_free_rooms



def get_room_curr_free(buildingID, roomID, time_int, day, week):

    # Get current time
    # curr_time = list(map(int, strftime("%H:%M", gmtime()).split(":")))
    # to_int = curr_time[0]*2
    # if curr_time[1] >= 30:
    #     to_int += 1
        
    # Get room
    room = get_room_from_day_week(buildingID, roomID, day, week)
    
    # Check if its free
    if time_int in room:
        return True
    else:
        return False


def get_all_room_names(buildingID):

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    

    # Do a search for building id first
    try:
        query = c.execute('''SELECT DISTINCT roomName FROM {}'''.format(buildingID))
    except sqlite3.OperationalError:

        # Otherwise use its name
        building_mapping = get_all_buildings_mapping()

        if buildingID not in building_mapping:
            conn.close()
            return None
        else:            
            try:
                query = c.execute('''SELECT DISTINCT roomName FROM {}'''.format(buildingID))
            except sqlite3.OperationalError:
                conn.close()
                return None

    data = [room[0] for room in query]
    conn.close()
    return data
    

def get_all_room_ids(buildingID):

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # Do a search for building id first
    try:
        query = c.execute('''SELECT DISTINCT roomID FROM {}'''.format(buildingID))
    except sqlite3.OperationalError:

        # Otherwise use its name
        building_mapping = get_all_buildings_mapping()

        if buildingID not in building_mapping:
            conn.close()
            return None
        else:            
            try:
                query = c.execute('''SELECT DISTINCT roomID FROM {}'''.format(buildingID))
            except sqlite3.OperationalError:
                conn.close()
                return None

    data = [room[0] for room in query]
    conn.close()
    return data

def get_all_room_mapping(buildingID):

    # Connect to database
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    # Do a search for building id firstz6
    try:
        query = c.execute('''SELECT DISTINCT roomName, roomID FROM {}'''.format(buildingID))
    except sqlite3.OperationalError:

        # Otherwise use its name
        building_mapping = get_all_buildings_mapping()

        if buildingID not in building_mapping:
            conn.close()
            return None
        else:            
            try:
                query = c.execute('''SELECT DISTINCT roomName, roomID FROM {}'''.format(buildingID))
            except sqlite3.OperationalError:
                conn.close()
                return None

    
    data = [[room[0], room[1]] for room in query]
    conn.close()
    return data

# print (get_all_buildings_mapping())
# print (get_rooms_from_building("B16", 2, 1))
print (get_all_room_ids("K17"), len(get_all_room_ids("K17")))
print (get_rooms_from_building("K17", 5, 6), len(get_rooms_from_building("K17", 3, 1)))
# print (get_free_rooms_from_building("B16", 22, 2, 1))
# print (get_buildings_free(20, 2, 1))
# print (get_room_from_day_week)
# print (get_all_building_ids())
# print (get_all_building_mappings_parsed())

# print (get_all_room_mapping("K17"))