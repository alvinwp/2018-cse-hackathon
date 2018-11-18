#!/bin/env python3
# import libraries
#need pip to install lxml to use soup parser
from bs4 import BeautifulSoup
import re
import requests

# term format: Term [Term no.]
# prior to 2018 format: Sem [Sem no.]
# can be found from classutil src


#testing info 2018 s2ARCH has half hour classes
#2018 s2 EDST has weird courses and also has one with 3 days
#2018 s2 
termStr = "Term 1" 

dayMap = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 6, 'Sun': 7}


courseInfo = {'name' : 'Error', "id" : 'Error'}
classInfo = {'comp': '', 'sect': '', 'class': '', 'type': '', 'status': '', 'cap': '', 'perc': '', 'times': None }
logReason = ''
logf = open('logfile', 'w')


def logLine(line):
    logf.write(line + '\n')

def getUrlList():
    # Get all URLs to parse
    # rootUrl = "https://nss.cse.unsw.edu.au/sitar/classes2018/" #for archived courses
    rootUrl = "http://classutil.unsw.edu.au/" #current
    indexUrl = rootUrl + 'index.html'
    htmlSrc = requests.get(indexUrl).content
    soup = BeautifulSoup(htmlSrc, "lxml")

    urls = []
    fac_tr_list = soup.findAll('tr', {'class':['rowLowlight', 'rowHighlight']})
    for faculty in fac_tr_list:
        terms = faculty.findAll('td')
        #print(faculty)
        for term in terms:
            
            if term.string == termStr:
                urls.append(rootUrl + term.find('a')['href'])
    return urls

def extractCourseName(row):
    global courseInfo
    global logReason
    cols = row.findAll('td')
    for col in cols:
        if 'class' in col.attrs:
            # logReason = 'COLUMN' + str(row) + str(courseInfo)
            if 'cucourse' in col['class'] and 'colspan' in col.attrs:
                if col['colspan'] == '6':
                    courseInfo['name'] = col.string
                else:
                    courseInfo['id'] = col.find('b').string

def isValidWeek(string):
    global logReason
    #print(string)
    if string == '< 1':
        logReason = 'week: w< 1'
        return False
    if 'N' in string:
        logReason = '\n==========!!!\n' + 'Special case, week: N[1,2,3]'
        return False
    return True

def extractBrackets(string):
    global logReason
    brackets = {}
    brackets['location'] = ''
    string = re.sub(r"\s+$", '', string)
    string = re.sub(r"^\s+", '', string)

    if string[0] != 'w':
        brackets['location'] = string
        brackets['weeks'] = [i for i in range(1, 14)]
    else:
        string = string[1:] #remove the 'w'

        #get the location, this is always after a comma then space
        match = re.search(r', (.+)\s*$', string)
        if(match == None or 'See School' in match.group(1)):
            logReason = 'week: no Location'
            return
        brackets['location'] = match.group(1)
        string = re.sub(r', .+\s*$', '', string)
        

        #get weeks
        weekValues = string.split(',')
        brackets['weeks'] = []
        for i in range(len(weekValues)): 
            if isValidWeek(weekValues[i]) == False:
                return None
            match = re.fullmatch(r'^\s*(\d+)-?(\d+)?\s*$', weekValues[i])
            if match == None:
                print('match error: ' + string + ' failed match')
                logf.close()
                exit()
            startWeek = match.group(1)
            endWeek = match.group(2)

            # end week empty case
            if endWeek == None or endWeek == '':
                brackets['weeks'].append(startWeek)
            #end week with a value
            else:
                for i in range(int(startWeek), int(endWeek)):
                    brackets['weeks'].append(i)
            #print('WEEKS', startWeek, endWeek)
    return brackets

def daysToArr(string):
    days = string.split(' ')
    return [dayMap[day] for day in days]

def cleanTime(startTime, endTime):
    if ':' not in startTime:
        startTime += ':00'
    if endTime == None or endTime == '':
        pattern = r'^(\d+):(\d+)$'
        match = re.fullmatch(pattern, startTime)
        assert(match)
        startHr = int(match.group(1))
        startMin = match.group(2)
        # assume that no classes pass over midnight
        endTime = str(startHr+1) + ":" + startMin
    elif ':' not in endTime:
        endTime += ':00'
    return (startTime, endTime)

def timeToArray(startTime, endTime):
    pattern = r'^(\d+):(\d+)$'
    match = re.fullmatch(pattern, startTime)
    assert(match)
    startHr = int(match.group(1))
    startMin = int(match.group(2))
    match = re.fullmatch(pattern, endTime)
    assert(match)
    endHr = int(match.group(1))
    endMin = int(match.group(2))

    #handle weird case where 00-00
    if startHr == 0 and endHr == 0:
        return [i for i in range(1, 49)] #1-48
    #round difference to nearest 30 min
    minDiff = round((endMin - startMin) / 30.0) / 2.0
    hrDiff = (endHr - startHr) + minDiff
    
    #round start time to nearest 30 min
    if(startMin):
        startHr += round(startMin/30.0) / 2.0
    times = []
    print(int(startHr*2),  int((startHr+hrDiff)*2))
    for i in range(int(startHr*2), int((startHr+hrDiff)*2), 1):
        times.append(i)
    assert(len(times))
    return times


def parseTimes(string):
    global logReason
    #print(string)
    string = re.sub(r"\s+Comb\/w.+$", '', string)
    string = re.sub(r"\s+$", '', string)

    if(string == ''):
        logReason = 'string: Empty string'
        return None
    
    times = string.split(';')
    for time in times:
        match = re.fullmatch(r"^\s*(.*)\s+(\d+:?\d*)-?(\d*?:?\d*).?\s+\((.*)\)\s*$", time)
        if match == None:
            print('match error: ' + time + ' failed match')
            logf.close()
            exit()
        days = match.group(1)
        startTime = match.group(2)
        endTime = match.group(3)
        brackets = match.group(4)

        #print(location)
        print(days, startTime, endTime, brackets)
        brackets = extractBrackets(brackets)
        if(brackets == None):
            return None
        print(days, daysToArr(days))
        (startTime, endTime) = cleanTime(startTime, endTime)
        print(startTime, endTime, timeToArray(startTime, endTime))
        #if(len(daysToArr(days)) > 1):
            #print(string, daysToArr(days))
    return None

def hasLocation(row, cols):
    global logReason
    global classInfo
    global courseInfo
    if len(cols[7].contents) < 1:
        logReason = 'string: Empty String'
        return False
    if cols[7].contents[0] == '':
        logReason = 'string: Empty String'
        return False
    if classInfo['status'].startswith('Closed'):
        logReason = 'status: Closed'
        return False
    if classInfo['status'].startswith('Stop'):
        logReason = 'status: Stop'
        return False
    if classInfo['status'].startswith('Canc'):
        logReason = 'status: Canc'
        return False
    if 'CRS' in classInfo['comp']:
        logReason = 'comp: course enrollment (not a class)'
        return False
    if 'WEB' in classInfo['sect']:
        logReason = 'sect: WEB course'
        return False
    if 'N/A' in classInfo['perc']:
        logReason = 'perc: N/A percentage'
        return False
    if 'even' in cols[7].contents[0] or 'odd' in cols[7].contents[0]: #special case even weeks specified
        logReason = '\n==========!!!\n' + 'Special case, may require manual entry' + "odd or even in contents"
        return False
    return True

def extractClassInfo(row): 
    global classInfo
    #print(row)
    cols = row.findAll('td')
    assert(len(cols) == 8)
    classInfo['comp'] = cols[0].string
    classInfo['sect'] = cols[1].string
    classInfo['class'] = cols[2].string
    classInfo['type'] = cols[3].string
    classInfo['status'] = cols[4].string
    classInfo['cap'] = cols[5].string
    classInfo['perc'] = cols[6].string
    #print(courseInfo, 'col 7 ' + cols[7].string)
    if(hasLocation(row, cols)):
        classInfo['times'] = parseTimes(cols[7].contents[0])
    else:
        classInfo['times'] = None

def parseTable(table):
    global logReason
    global courseInfo
    global classInfo
    # ign non-class tables
    if(table.find('td', {'class': 'cucourse'}) == None):
        return
    rows = table.findAll('tr')
    for row in rows:
        if 'class' in row.attrs and ('rowLowlight' in row['class'] or 'rowHighlight' in row['class']):
            
            extractClassInfo(row)
        else:
            extractCourseName(row)
        if(logReason != ''):
            logLine(logReason + "\t" + str(courseInfo) + "\t" + str(classInfo) + "\t" + str(row.contents))
            logReason = ''

urls = getUrlList()

#urls = ['https://nss.cse.unsw.edu.au/sitar/classes2018/COMP_S2.html']

for url in urls:
    htmlSrc = requests.get(url).content
    soup = BeautifulSoup(htmlSrc, "lxml")
    tables = soup.findAll('table')
    print(url)
    for table in tables:
        parseTable(table)

logf.close()

#print(fac_tr_list)


