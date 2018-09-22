import time
import datetime


timee = time.time()
print(timee)


# time given as epoch
def get_day(time):
    time = datetime.datetime.fromtimestamp(time)
    print(time.weekday()+1)

date_time = '30.08.2011 11:05:02'
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
print(epoch)

get_day(epoch)




# start = 23-Jul-2018
# mid = 22-Sep-2018

# date.weekday()

# datetime(year, month, day, hour, minute, second, microsecond, tzinfo)
# timestamp = datetime.datetime(2017, 12, 1, 0, 0).timestamp()



# #!/usr/bin/python
# import time

t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
t = time.mktime(t)
print(time.strftime("%b %d %Y %H:%M:%S", time.localtime(t)))
# time.localtime

# converts time to string
# month a
