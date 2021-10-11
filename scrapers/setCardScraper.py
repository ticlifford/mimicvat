import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import sqlite3

# this scrapes card information from scryfall for the "cards" table
# the input is a csv with every card set as a code (example, 'aer' is aether revolt)
#it scrapes each set for things like the name, power, toughness etc and inserts that into an sql table called cards

dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
#dbPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO.db'
#dbPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO_test.db'
csvPath = '/home/timc/flask_project/flask_app/setNames.csv'
#csvPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/setNames.csv'

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

        tcg_id = None
        if 'tcgplayer_id' not in obj.keys():
            print('no tcgid')
            None

        else:
            tcg_id = obj['tcgplayer_id']

        cm_id = None
        if 'cardmarket_id' not in obj.keys():
            print('no cmid')
            None
        else:
            cm_id = obj['cardmarket_id']

        #dual face cards

        if obj['layout'] == 'modal_dfc':
            print('modal dfc card found')
            try:
                #inside card_faces, theres a list of two dictionaries
                #accessing each card face by calling [0] or [1]
                #the sql insert should be called for both faces with their respective object indexes
                print(obj['card_faces'][0]['name'],"DFC")
                print(
            obj['id'],
            str(obj['name']),
            obj['cmc'],
            obj['card_faces'][0]['mana_cost'],
            power,
            toughness,
            str(obj['card_faces'][0]['colors']),
            obj['set'],
            obj['card_faces'][0]['type_line'],
            obj['card_faces'][0]['image_uris']['normal'],
            str(obj['foil']),
            str(obj['nonfoil']),
            str(obj['digital']),
            rarity,
            str(obj['reserved']),
            tcg_id,
            cm_id
                )
                c.execute('insert or ignore into CARDS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
            obj['id'],
            str(obj['name']),
            obj['cmc'],
            obj['card_faces'][0]['mana_cost'],
            power,
            toughness,
            str(obj['card_faces'][0]['colors']),
            obj['set'],
            obj['card_faces'][0]['type_line'],
            obj['card_faces'][0]['image_uris']['normal'],
            str(obj['foil']),
            str(obj['nonfoil']),
            str(obj['digital']),
            rarity,
            str(obj['reserved']),
            tcg_id,
            cm_id
            ))
            except:
                print('could not complete dfc faces print')
        else:



            # db command to write object to db
            try:
                c.execute('insert or ignore into CARDS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
                obj['id'],
                str(obj['name']),
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
                rarity,
                str(obj['reserved']),
                tcg_id,
                cm_id
                ))
                print("insert was a SUCCESS")
            except:
                print('could not add to db:',obj['name'])

    try:
        checkPage(data)
    except:
        print('could not check for pages')

try:
    print('connecting to db')
    cardsDb = sqlite3.connect(dbPath)
# cardsDb = sqlite3.connect('C:\\users\\tim\\desktop\\CARDINFO.db')
    c = cardsDb.cursor()
except:
    print('could not connect to dbPath')



with open(csvPath, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print('set scraping:',line[0])
        setGeneration(line[0])


cardsDb.commit()
print('im closing the db')
cardsDb.close()
