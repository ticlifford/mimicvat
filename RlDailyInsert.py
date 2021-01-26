
# this is a script to add the "reserved list" boolean to the cards table
# this will scrape scryfall for every card, check if reserved is true or false, and the write the value to its cardid

#first, to add the column "reserved" to the cards table, run the sql command "alter table cards add RESERVED text;"

import datetime as dt
from datetime import date
import time
from dateutil.rrule import rrule, DAILY
import sqlite3

dbPath = 'CARDINFO.db'
#dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
cardsDb = sqlite3.connect(dbPath)
c = cardsDb.cursor()

# these are date ranges to run the batch updater
"""
# start
a = date(2020, 7, 9)
# end
#b = date(2019, 6, 18)
b = date(2021, 1, 22)
"""

# the dictionary that gets inserted to the database
compiled_dic = {}

# function that takes a date and returns the added value
def add_day(datetime):
    print('running add_day for :',datetime)
    datetime = str(datetime)
    try:
        print('running sql')
        collectionQuery = c.execute(f"select normprice from prices, cards where prices.id = cards.id and prices.datetime = '{datetime}' and cards.reserved = 'True' and cards.ONLINEONLY = 'False' ")
    except:
        print('could not query')
    day_value = 0
    for x in collectionQuery:
        #print(x)
        if x[0] is not None:
            day_value = day_value + x[0]
    day_value = round(day_value,2)
    print('day_value:',day_value)
    compiled_dic[datetime] = day_value
    return day_value

# batch running

# this is used to run a loop which adds up all previous values, from dates a to b
# (if you need to rebuild the database)
"""
for dt in rrule(DAILY, dtstart=a, until=b):
    datetime = dt.strftime("%Y-%m-%d")
    add_day(datetime)
"""

#get time from time
def getTime():
    try:
            ts = time.time()
            dateTime = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            return dateTime
    except:
            print('getTime didnt work')
            with open(fPath, 'a') as f:
                f.write('\n couldnt run getTime')

print('test getTime:',getTime())




#how to convert this one time update to the daily script:

#get time for today
today = getTime()
#run add_day for time(today)
add_day(today)
#for key value pair, execute insert sql
for key, value in compiled_dic.items():
    c.execute("insert or ignore into reservedhistory values (?,?)",(key,value))
    #print('key:',key)
    #print('value:',value)
"reservedhistory"

#commit and close
cardsDb.commit()
print('im closing the db')
cardsDb.close()
print('finished')
