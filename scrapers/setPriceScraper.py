import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys

def dataParse():
    for obj in data['data']:
        print(obj['name'])
        print(obj['prices']['usd'])
        print(obj['id'])

def checkPage(data):
    try:
        if data['has_more'] == True:
                print('I found another page of cards')
                jason_obj = urllib.request.urlopen(data['next_page'])
                data = json.load(jason_obj)
                dailyPrice(data)
    except:
        print('check page could not perform loop')

def setGeneration(set):
    print('the set is',set)
    url = "https://api.scryfall.com/cards/search?q=set%3D" + set
    print('sleeping now')
    time.sleep(.600)
    print('the url is',url)
    try:
        jason_obj = urllib.request.urlopen(url)
        data = json.load(jason_obj)
        dailyPrice(data)
    except:
        print('something went wrong with set',set)

def getTime():
        try:
                ts = time.time()
                dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                return dateTime
        except:
                print('getTime didnt work')
print('test getTime:',getTime())

def foilRatio():
        try:
                foilRatio = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])
                return foilRatio
        except:
                return None

def dailyPrice(data):
    for obj in data['data']:
        foilCalc = None
        usd = None
        foilUsd = None

        if obj['prices']['usd_foil'] == None:
                None
        else:
                foilUsd = obj['prices']['usd_foil']
        if obj['prices']['usd_foil'] == None or obj['prices']['usd']==None:
                foilCalc = None
        else:
                foilCalc = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])

        try:
                c.execute('insert into PRICES values (?,?,?,?,?)',(
                obj['id'],
                current_time,
                obj['prices']['usd'],
                obj['prices']['usd_foil'],
                foilCalc
                ))
        except:
                print('could not add to db')
                print( 'id:', obj['id'],'usd:' ,obj['prices']['usd'], 'foil:', obj['prices']['usd_foil'])
                sys.exit()
    checkPage(data)

def printDb():
        print('im printing the db here:')
        for row in c.execute('SELECT * FROM PRICES'):
                print(row)

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

current_time = getTime()

with open('setNames.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print('set scraping:',line[0])
        setGeneration(line[0])

cardsDb.commit()
print('im closing the db')
cardsDb.close()
