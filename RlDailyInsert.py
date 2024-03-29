

# This script compiles the daily RL value
# it is set up to run daily and insert into reservedhistory
# it also has a batch feature to rebuild the historic reservedhistory table given two dates

#first, to add the column "reserved" to the cards table, run the sql command "alter table cards add RESERVED text;"

import datetime as dt
from datetime import date
import time
from dateutil.rrule import rrule, DAILY
import sqlite3


# database connection setup

#dbPath = 'CARDINFO.db'
#dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbPath = 'G:/Documents/coding files/mimicvat_db_2023/mini_db/CARDINFO.db'
cardsDb = sqlite3.connect(dbPath)
c = cardsDb.cursor()

# the dictionary that gets inserted to the database
compiled_dic = {}

# function that takes a date and returns the added value
def add_day(datetime):
    print('running add_day for :',datetime)
    datetime = str(datetime)
    try:
        print('running sql')
        collectionQuery = c.execute(f"select normprice from prices, cards where prices.id = cards.id and prices.datetime = '{datetime}' and cards.reserved = 'True' and cards.ONLINEONLY = 'False' and cards.cardset not in ('cei','leb','lea','wc97','wc98','wc99','wc00','wc01','wc02','30a')")
        #collectionQuery = c.execute(f"select normprice from prices, cards where prices.id = cards.id and prices.datetime = '{datetime}' and cards.reserved = 'True' and cards.ONLINEONLY = 'False' and cards.cardset not in ('cei','w01')")
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





#get time from time
def getTime():
    try:
            ts = time.time()
            dateTime = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            return dateTime
    except:
            print('getTime didnt work')
            with open(fPath, 'a') as f:
                f.write('\n couldnt run getTime in RlDailyInsert')
try:
    print('test getTime:',getTime())
except:
    print('could not run getTime')


# batch operation

# this is used to run a loop which adds up all previous values, from dates a to b
# (if you need to rebuild the database)

# these are date ranges to run the batch updater


def date_range_collection(a,b):
    for dt in rrule(DAILY, dtstart=a, until=b):
        datetime = dt.strftime("%Y-%m-%d")
        add_day(datetime)

    for key, value in compiled_dic.items():
        c.execute("insert or ignore into reservedhistory values (?,?)",(key,value))
    cardsDb.commit()
    print('im closing the db')
    cardsDb.close()
    print('finished')


#"""
# start
a = date(2023, 6, 3)
# end
b = date(2023, 6, 13)

date_range_collection(a,b)

#"""




"""
# daily script:
try:
    print('running RLDailyInsert for today')
#get time for today
    today = getTime()

    #run add_day for time(today)
    add_day(today)

    #for key value pair, execute insert sql
    for key, value in compiled_dic.items():
        c.execute("insert or ignore into reservedhistory values (?,?)",(key,value))

    #commit and close
    cardsDb.commit()
    print('im closing the db')
    cardsDb.close()
    print('finished')
except:
    print('could not run RLDailyInsert for today')
"""
