import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import sqlite3
from db_location import dbLoc,csvPath,fullnamepath



#this small bit of code returns all the sets

url = 'https://api.scryfall.com/sets'
codenamepath = csvPath
dbpath = dbLoc

jason_obj = urllib.request.urlopen(url)
data = json.load(jason_obj)

try:
    cardsDb = sqlite3.connect(dbpath)
    c = cardsDb.cursor()
except:
    print('could not connect to db')

#this is a csv file to write into
#every 2 weeks this should run to collect the new sets
try:
    with open (codenamepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for obj in data['data']:
            """
            print(obj['code'])
            print(type(obj['code']))
            print(obj['name'])
            print(type(obj['name']))
            print(obj['released_at'])
            print(type(obj['released_at']))
            """
            print('inserting: ',obj['code'],obj['name'],obj['released_at'])
            csv_writer.writerow([obj['code']])

            try:
                c.execute('insert or ignore into CARDSET values (?,?,?)',(
                obj['name'],
                obj['code'],
                obj['released_at']
                ))
                print('sqlite3 insert worked')
            except:
                print('sqlite3 insert didnt work')
except:
    print('something went wrong with setNames.csv')

try:
    with open (fullnamepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for obj in data['data']:
            csv_writer.writerow([obj['name'].replace(" ", "-")])
except:
    print('something went wrong with setFullNames.csv')


print('set names collected')
try:
    cardsDb.commit()
    print('im closing the db')
    cardsDb.close()
except:
    print('something went wrong closing db. program is finished.')