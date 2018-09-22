# import libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def handle_page(soup):
    title = soup.find_all("td",{"class": "classSearchMinorHeading"})[0].getText()
    title = re.search(r'[A-Z]{4}[0-9]{4}', title)
    print(title.group(0))
    big_list_rooms = []

    for i,elem in enumerate(soup(text=re.compile(r'Class Nbr'))):
        info_dict = {}
        info_dict['course title'] = title
        table = elem.parent.parent.parent
        tr_list = table.find_all('tr')
        
        # get name

        name = tr_list[0].td.a['name']
        index_list = [1, 3, 5, 7]
        add_details(tr_list, index_list, info_dict)

        # Get Room information, may have multiple days/rooms
        room_index = 11
        td_list_labels = tr_list[room_index].findAll("td", {"class": "tableHeading"})
        td_list_data = tr_list[room_index].findAll("td", {"class": "data"})

        room_list = []
        for j, data in enumerate(td_list_data, 0):
            if (j % 5) == 0:
                # Empty dict
                if j == 0:
                    new_dict = {}
                else:
                    room_list.append(new_dict)
                    new_dict = {}
            new_dict[td_list_labels[j%5].getText()] = td_list_data[j].getText()
            if j == len(td_list_data)-1:
                room_list.append(new_dict)
        info_dict['rooms'] = room_list
        big_list_rooms.append(info_dict)
    return big_list_rooms, title
    # print(big_list_rooms)

# Parameters to DB
# --------------

# add_to_db():

# Building ID   - String
# Building Name - String
# Room ID       - String
# Room Name     - String
# Room Type     - String  
# Week          - Integer Array [13] *
# Day           - Integer (0-6) *
# Time          - Integer (0 - 2359) (

def add_to_db_helper(table, coursename):
    # Check for rooms in the table
    for room_dict in table['rooms']:
        time = room_dict.get('Time')

        # Get room details
        location = room_dict.get('Location')
        day = room_dict.get('Day')
        
        building_name, room_name = handle_building_names(room_dict.get("Location"))
        building_id = building_name
        room_id = room_name
    
        # Course name

        # Split by commas
        # Handle data from the weeks
        week = room_dict.get('Weeks')
        week_list = handle_weeks(week)


def handle_weeks(weeks):
    str_list = weeks.split(',')
    week_list = []
    for str_ in str_list:
        # week-week case
        if len(str_) > 2:
            m_ = re.findall('\d\d?-\d\d?', str_)
            for match in m_:
                ranges = match.split('-')
                lower = int(ranges[0])
                upper = int(ranges[1])
                print("lower" + ranges[0])
                print("upper" + ranges[1])
                week_list.extend(range(lower, upper+1))
        # singular week        
        else:
            # single week stuff
            week_list.append(int(str_))
    return week_list, title

def handle_building_names(b):

    # "UNSW Business School G21 (K-E12-G21)",
    # "Rex Vowels Theatre (K-F17-LG3)",
    # "Mathews 102 (K-F23-102)",
    # "E26 Teaching Lab 11 (K-E26-1101)"

    r = r"(.*?)(\s[0-9]*?\s|\s)\((.*)\)"

    match = re.search(r, b)

    if match:
        building_name = match.group(1).strip()
        building_id = match.group(3).strip()

        # Strips of room id
        building_name = building_name.strip(building_id.split("-")[-1]).strip()
        print(building_name, ":", building_id)
        name_list = building_id.split('-')
        building_name = name_list[1]
        room_name = name_list[2]
            
        return building_name, room_name

    # add_to_db():

    # Building ID   - String
    # Building Name - String
    # Room ID       - String
    # Room Name     - String
    # Room Type     - String
    # Time          - Integer Array
    # Week          - Integer Array


# Adds table field information into a dict format
# label -> data
# @param index_list, index of tr's with information to consider
# @param tr_list, list of tr soup elements in table of interest
# @param info_dic, where label -> data will be stored
def add_details(tr_list, index_list, info_dict):
    for i in index_list:
        td_list_labels = tr_list[i].findAll("td", {"class": "label"})
        td_list_data = tr_list[i].findAll("td", {"class": "data"})
        for j, label in enumerate(td_list_labels, 0):
            info_dict[label.getText()] = td_list_data[j].getText()

#'course title': 'ELEC1111 Electrical and Telecommunications Engineering', 
# 'Offering Period': '23/07/2018 - 28/10/2018', 'Class Nbr': '5572', 
# 'Section': 'H11A', 'Status': 'Open', 'Meeting Dates': 'Standard dates', 
# 'Teaching Period': 'T2 - Teaching Period Two', 'Consent': 'Consent not required', 
# 'Instruction Mode': 'In Person', 'Activity': 'Tutorial', 'Census Date': '31/08/2018',
#  'Enrols/Capacity': '95/120'}


# Try beautiful soup

# page_url = 'http://timetable.unsw.edu.au/2018/ACCT1511.html'
page_url = 'http://timetable.unsw.edu.au/2018/ELEC1111.html#S1-5346'
page = urlopen(page_url)
soup = BeautifulSoup(page, "lxml")
big_list_rooms, title = handle_page(soup)

for element in big_list_rooms:
    add_to_db_helper(element, title)