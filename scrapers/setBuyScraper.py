import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys


def getTime():
        try:
                ts = time.time()
                dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                return dateTime
        except:
                print('getTime didnt work')

def setNameActivator():
    with open('setFullNames.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            print('set scraping:',line[0])
            scrape(line[0])


def scrape(setName):
    url = "https://shop.tcgplayer.com/price-guide/magic/" + setName

    try:
        html = urllib.request.urlopen(url).read()
        soup = b(html, 'html.parser')
        """
        cards = soup.find('tr', {'class' : 'even'})
        buyP = cards.find('td', {'class' : 'buylistMarketPrice'}).get_text()
        print(buyP)
        """
        #even
        for x in soup.find_all('tr', {'class' : 'even'}):
            cardName = x.find('div', {'class' : 'productDetail'}).get_text().rstrip().strip()
            buyPrice = x.find('td', {'class' : 'buylistMarketPrice'}).get_text().rstrip().strip()
            print(cardName)
            print(buyPrice[1:])
            cardNames.append(cardName)
            if buyPrice == u'\u2014':
                cardBuyPrices.append(float(0))
            else:
                cardBuyPrices.append(float(buyPrice[1:]))



        for x in soup.find_all('tr', {'class' : 'odd'}):
            cardName = x.find('div', {'class' : 'productDetail'}).get_text().rstrip().strip()
            buyPrice = x.find('td', {'class' : 'buylistMarketPrice'}).get_text().rstrip().strip()
            print(cardName)
            print(buyPrice[1:])
            cardNames.append(cardName)
            if buyPrice == u'\u2014':
                cardBuyPrices.append(float(0))
            else:
                cardBuyPrices.append(float(buyPrice[1:]))
    except:
        print('something went wrong with scrap URL')


def dbPush():
    for i in range(0,len(cardNames)):
        try:
            c.execute('insert into BUYLIST values (?,?,?)',(
            cardNames[i],
            time,
            cardBuyPrices[i]
            ))
        except:
            print('could not add to db')
            sys.exit()



cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

time = getTime()
cardNames = []
cardBuyPrices = []

setNameActivator()
dbPush()
print('card names:')
print(cardNames)
print(cardBuyPrices)


cardsDb.commit()
print('im closing the db')
cardsDb.close()

