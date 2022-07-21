from readline import insert_text
import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import sqlite3


dbPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO.db'
csvPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/setNames.csv'

def printDb():
        print('im printing the db here:')
        for row in c.execute('SELECT * FROM CARDS'):
                print(row)
def printAbandon():
        print('im printing Abandon here:')
        for row in c.execute('SELECT * FROM CARDS where name="Abandon the Post" and cardset="mid"'):
                print(row)

def update_Abandon():
    try:
        c.execute('insert or replace into CARDS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
        '983da138-f0f5-46c4-90c2-d3c34cc37d1f', 'Abandon the Post', 2.0, '{1}{R}', None, None, "['R']", 'mid', 'sorcery', 'https://c1.scryfall.com/file/scryfall-cards/normal/front/9/8/983da138-f0f5-46c4-90c2-d3c34cc37d1f.jpg?1634350355', 'True', 'True', 'False', 'common', 'False', 248251.0, 575051.0, 0)
        )
    except:
        print('error insert updating Abandon the Post')

try:
    print('connecting to db')
    cardsDb = sqlite3.connect(dbPath)
    c = cardsDb.cursor()
except:
    print('could not connect to dbPath')


try:
    #printDb()
    update_Abandon()
except:
    print('could not update_Abandon')
    #print('cant print db')
try:
    printAbandon()
except:
    print('error printing')


try:
    cardsDb.commit()
    print('im closing the db')
    cardsDb.close()
except:
    print('cant close db')