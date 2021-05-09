import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import sqlite3

# this scrapes card information from scryfall for the "cards" table
# the input is a csv with every card set. Then it runs through each card set code


#dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbPath = 'CARDINFO.db'
#csvPath = '/home/timc/flask_project/flask_app/setNames.csv'
csvPath = 'setNames.csv'

def printDb():
        print('im printing the db here:')
        for row in c.execute('SELECT * FROM CARDS'):
                print(row)

def setGeneration(set):
    print('the set is',set)
    url = "https://api.scryfall.com/cards/search?q=set%3D" + set
    print('sleeping now')
    time.sleep(.600)
    print('the url is',url)
    try:
        jason_obj = urllib.request.urlopen(url)
        data = json.load(jason_obj)
        addCards(data)
    except:
        print('something went wrong with set',set)

def checkPage(data):
    # this api is paginated into 175 card objects
    try:
        if data['has_more'] == True:
            #print(obj['has_more'])
                print('I found another page of cards')
                jason_obj = urllib.request.urlopen(data['next_page'])
                data = json.load(jason_obj)
                addCards(data)
    except:
        print('check page could not perform loop')


def addCards(data):
    for obj in data['data']:
    # if-statements to figure out if data is missing
        toughness = None
        if 'toughness' not in obj.keys():
            None
        else:
            toughness = obj['toughness']

        power = None

        if 'power' not in obj.keys():
            None
        else:
            power = obj['power']

        cmc = None
        if 'cmc' not in obj.keys():
            None
        else:
            cmc = obj['cmc']
        
        rarity = None
        if 'rarity' not in obj.keys():
            None
        else:
            rarity = obj['rarity']



        # db command to write object to db
        try:
            print('inserting id:',obj['id'])
            print('reserved val:',str(obj['reserved']))
        except:
            print('could not get card id and or reserved val')
        try:
            c.execute('update CARDS set reserved = ? where id = ?',(
            str(obj['reserved']),
            obj['id']
            ))
        except:
            print('could not add to db:',obj['name'])

    try:
        checkPage(data)
    except:
        print('could not check for pages')



# make a database connection
cardsDb = sqlite3.connect(dbPath)
# cardsDb = sqlite3.connect('C:\\users\\tim\\desktop\\CARDINFO.db')
c = cardsDb.cursor()

"""
#testing sql database
first_row = c.execute('SELECT * FROM cards ORDER BY ROWID ASC LIMIT 1')
for x in first_row:
    print(x)
"""




with open(csvPath, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print('set scraping:',line[0])
        setGeneration(line[0])


cardsDb.commit()
print('im closing the db')
cardsDb.close()
