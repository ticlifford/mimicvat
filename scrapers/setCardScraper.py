import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import sqlite3



# functions:

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


# lists for this api are paginated into 175 card objects
# if a set has more it is broken into more api calls, which is inside the dictionary as a url
# here, I check to see if the data "has more," and if it does I extract the URL and run that url too

def checkPage(data):
    try:
        if data['has_more'] == True:
            #print(obj['has_more'])
                print('I found another page of cards')
                # do an addCards with obj['next_page']
                # print('the next page url:',data['next_page'])
                jason_obj = urllib.request.urlopen(data['next_page'])
                data = json.load(jason_obj)
                addCards(data)
    except:
        print('check page could not perform loop')


def addCards(data):
    for obj in data['data']:
        # print the object name
        # print('obj name:',obj['name'])
        # time.sleep(.050)


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

# sqlite3 command to write object to db
        try:
            # print(type(rarity))
            c.execute('insert or ignore into CARDS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
            obj['id'],
            obj['name'],
            cmc,
            obj['mana_cost'],
            power,

            toughness,
            str(obj['colors']),
            obj['set'],
            obj['type_line'],
            obj['image_uris']['normal'],

            str(obj['foil']),
            str(obj['nonfoil']),
            str(obj['digital']),
            rarity
            ))
        except:
            print('could not add to db:',obj['name'])


    try:
        checkPage(data)
    except:
        print('could not check for pages')








# connecting to db (this should probably be inside the dailyPrice loop to allow the commit and close functions)
cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()


# this opens the set names, and adds the values to the database for all cards found in all sets
with open('setNames.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print('set scraping:',line[0])
        setGeneration(line[0])




cardsDb.commit()
print('im closing the db')
cardsDb.close()