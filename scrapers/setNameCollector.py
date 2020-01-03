import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import sqlite3



#this small bit of code returns all the sets

url = 'https://api.scryfall.com/sets'

jason_obj = urllib.request.urlopen(url)
data = json.load(jason_obj)

cardsDb = sqlite3.connect('C:\\users\\tim\\desktop\\CARDINFO.db')

# cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

c.execute('select * from CARDSET limit 1')
print(c.fetchall())

#this is a csv file to write into
#every 2 weeks this should run to collect the new sets
with open ('setNames.csv', 'w', newline='') as csv_file:
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

with open ('setFullNames.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    for obj in data['data']:
        csv_writer.writerow([obj['name'].replace(" ", "-")])

print('set names collected')

cardsDb.commit()
print('im closing the db')
cardsDb.close()