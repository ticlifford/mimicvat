
# this is a script to add the "reserved list" boolean to the cards table
# this will scrape scryfall for every card, check if reserved is true or false, and the write the value to its cardid

#first, to add the column "reserved" to the cards table, run the sql command "alter table cards add RESERVED text;"

import datetime as dt
from datetime import date
from dateutil.rrule import rrule, DAILY
import sqlite3

#dbPath = 'CARDINFO.db'
dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
cardsDb = sqlite3.connect(dbPath)
c = cardsDb.cursor()

# start
a = date(2019, 6, 11)
# end
#b = date(2019, 6, 18)
b = date(2020, 7, 9)

compiled_dic = {}

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

for dt in rrule(DAILY, dtstart=a, until=b):
    datetime = dt.strftime("%Y-%m-%d")
    add_day(datetime)

print('finished')

for key, value in compiled_dic.items():
    c.execute("insert into reservedhistory values (?,?)",(key,value))
    #print('key:',key)
    #print('value:',value)
"reservedhistory"

cardsDb.commit()
print('im closing the db')
cardsDb.close()