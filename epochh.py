import time
import datetime
import re

# time given as seconds from epoch
def get_day():
    curr_day = int(time.strftime("%w", time.localtime(time.time())))
    if curr_day == 0:
        return 7
    return curr_day+1

# current time object

# def week_difference(day, month, year):
#     now = datetime.date.today() 
#     dt = datetime.datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), '%Y-%m-%d')
#     print(now - dt)

def getWeekInt():
    # current YEAR WEEK is 38
    # current UNI WEEK is 9
    # 38-9 = 29
    WEEK_BUFFER = 29
    
    curr_week = int(time.strftime("%W", time.localtime(time.time())))
    
    # MID SEM WEEK is YEAR WEEK 39
    # if midsem break return -1
    if curr_week == 39:
        return -1
    # so add 1 week buffer after midsem break
    elif curr_week >= 40:
        WEEK_BUFFER = WEEK_BUFFER + 1
        
    return curr_week - WEEK_BUFFER        

def getTimeInt():
    curr_time = time.strftime("%H:%M", time.localtime(time.time()))
    
    s = re.search('([0-9]+):([0-9]+)', curr_time)
    
    if int(s.group(2)) <= 30:
        int_time = int(s.group(1))*2
    else:
        int_time = int(s.group(1))*2 + 1

    return int_time


def get_info():
    return getTimeInt(), get_day(), getWeekInt()

print(get_info())
# start = 23-Jul-2018
# mid = 22-Sep-2018

# date.weekday()

# datetime(year, month, day, hour, minute, second, microsecond, tzinfo)
# timestamp = datetime.datetime(2017, 12, 1, 0, 0).timestamp()



# t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
# t = time.mktime(t)
# print(time.strftime("%b %d %Y %H:%M:%S", time.localtime(t)))
# time.localtime

# converts time to string
# month 
