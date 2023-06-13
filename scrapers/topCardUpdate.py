# Daily RL percent changes



import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys
from db_location import dbLoc

dbPath = dbLoc

#connect to db
try:
    print('connecting to db')
    cardsDb = sqlite3.connect(dbPath)
    cur = cardsDb.cursor()
except:
    print('could not connect to db')



# collecting dates to run SQL
try:
    print('collecting most recent date')
    today_date = cur.execute("select max(datetime) from prices")
    today_date  = cur.fetchone()
    newdate = today_date[0].replace("-","/")
    time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
    print('time element:',time_element.date())
    last_week = time_element - datetime.timedelta(days=7)
    todays_date = time_element
    print('todays_date',todays_date)
    yesterday_date = time_element - datetime.timedelta(days = 1)
    last_week = last_week.date()
    print('last week: ',last_week)
except:
    print('could not collect recent dates')

# running SQL fetch
try:
    avg_norms = cur.execute("select avg(normprice),cards.id from prices, cards where prices.id=cards.id and datetime>(?) and datetime<(?) group by cards.id",(last_week,yesterday_date,))
    print('printing avg norms')
    rows2 = cur.fetchall()
except:
    print('could not select averages')

try:
    #print(rows2)
    #print('row2 can print here')
    None
except:
    print('could not print rows2')
try:
    print('creating dict')
    rl_dict = {}
    for row in rows2:
        if row[0] is None:
            rl_dict[row[1]] = 0.0
        else:
            rl_dict[row[1]] = row[0]
except:
    print('could not create dict')

try:
    #print('printing rl_dict')
    #print(rl_dict)
    None
except:
    print('could not print rl_dict')
try:
    #today_cur = cur.execute("select normprice,cards.id from cards, prices where cards.id=prices.id and length(cards.cardset) < 4 and cards.reserved='True' and cards.onlineonly = 'False' and cards.nonfoil = 'True' and datetime=(?)",(todays_date.date(),))
    today_cur = cur.execute("select normprice,cards.id from cards, prices where cards.id=prices.id and datetime=(?)",(todays_date.date(),))
except:
    print('could not select today_date val')
try:
    print('fetching todays normprice to divide with')
    #rows3 = cur.fetchmany(5)
    rows3 = cur.fetchall()
    print('rows3: ',rows3)
    for row in rows3:
        # if the id is in rl_dict
        print('row:',row)
        if row[1] in rl_dict:
            print('row 1 was in dict')
            print(row[1])
            # if today's normalprice is None, then just make the value for dict 0.0
            # otherwise, move on and collect the week_avg then do the math to figure out what its replaced with
            if row[0] is None:
                print('row 0 was none')
                rl_dict[row[1]] = 0.0
            else:
                print('row 0 was not none, collecting week_avg')
                week_avg = rl_dict[row[1]]
                #print('week avg:',week_avg)
                #print('todays val:', row[0])
                #print('divided:',row[0]/week_avg)
                try:
                    if week_avg is 0.0 or week_avg is None:
                        #print('week_avg was 0.0 or none')
                        rl_dict[row[1]] =0.0
                    else:
                        #print('updating rl_dict with new divided number')
                        percent_change = row[0]/week_avg
                        rl_dict[row[1]] = percent_change
                except:
                    #print('something else didnt work so updating with 0.0')
                    rl_dict[row[1]] =0.0
except:
    print('could not update dict')

try:
    print('dict:')
    print(rl_dict)
    None
except:
    print('could not print new dict')


# add to SQL table called RESERVECHANGE using insert or update

try:
    rl_list = []
    print('converting dict to list for SQL insert')
    for key, val in rl_dict.items():
        #rl_list.append([key,"{:.0%}".format(val-1)])
        #print('key and val:')
        try:
            None
            #print(key)
        except:
            print('could not print key')
        try:
            None
            #print(val)
        except:
            print('could not print val')
        rl_list.append([key,val])
except:
    print('could not convert dict to list')
print('list:',rl_list)

try:
    print('inserting to sql')
    print(type(rl_list[0][0]),type(rl_list[0][1]))
    for card in rl_list:
        cur.execute("insert or replace into PRICECHANGE values (?,?)", (card[0],card[1]))
except:
    print('could not insert to sql')


cardsDb.commit()
print('im closing the db')
cardsDb.close()

# selects top 10 changes this week
#select cards.name, RESERVEDCHANGE.change from cards, RESERVEDCHANGE where cards.ID=RESERVEDCHANGE.id order by RESERVEDCHANGE.change desc limit 10;