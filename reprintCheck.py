import urllib.request
import json
import requests
import csv
import time
import datetime
from datetime import datetime
import sqlite3
import sys
import statistics as stats

def reprintAverage(cardid):

    # collect all the print dates for the card id and add to a list

    dateList = []
    dayList = []


    cardName = c.execute('select cards.name from cards where cards.id = ?', (cardid,))
    print('card name: ',cardName.fetchone)
    rows = c.execute('select cards.name, CARDSET.NAME, CARDSET.RELEASEDATE, PRICES.NORMPRICE from cards, CARDSET, prices where cards.ID==prices.ID and cards.CARDSET == CARDSET.CODE and cards.name == "Sol Ring" order by prices.NORMPRICE desc')
    # loop through the list and create another list of days between those days
    for row in rows:
        print(row[2])
        dateList.append(row[2])
    #get the average of those and return it as an int
    dateList.sort()
    print(dateList)
    for i in range(0,(len(dateList)-2)):
            
        d1 = datetime.strptime(dateList[i], "%Y-%m-%d")
        d2 = datetime.strptime(dateList[i+1], "%Y-%m-%d")
        daynum = abs((d2 - d1).days)
        print('days:', abs((d2 - d1).days))
        dayList.append(daynum)
    print(stats.mean(dayList))

# connect to database

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

# place function here

reprintAverage("2ae1bb79-a931-4d2e-9cc9-a06862dc5cde")


# commit and close database
cardsDb.commit()
cardsDb.close()