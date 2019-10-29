import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import sqlite3


#This is a webscraper made with beautifulsoup that scrapes a website called edhrec.com, and grabs the json values I want
#I scrape the html of the page and grab two values: the name of the card, and a number which says how many people have used that card. This indicates how popular and thus important it is
#I'm going to use this data later on to make judgements and analysis, but for now this is a demo to learn how to use beautifulsoup (which was very helpful)

def edhChecker(nameV,numV):
        try:
                c.execute('insert into EDHPOP values (?,?)',(
                nameV,
                numV
                ))
        except:
                print('could not add to db')

url = 'https://edhrec.com/sets/aer'

html = urllib.request.urlopen(url).read()

cardName = []
cardLabel = []
soup = b(html, 'html.parser')
s=soup.find('script')

scripts = soup.find_all('script')
dic = scripts[-3]
dic = str(dic)
cardDic = dic[26:-10]

cardDic = json.loads(cardDic)
oGdic = cardDic
cardDic = cardDic['cardlists']


cardDic = cardDic[0]

cardDic = cardDic['cardviews']

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

#this is the loop that's doing most of the work
#I grab the 'name' and 'label' from the json
for x in oGdic['cardlists']:
    for y in x['cardviews']:
        for key, val in y.items():
            if key =='name':
                print('theval:',val)
                cardName.append(val)
                nameV = val
            if key =='label':
                print('the label:',val)
                cardLabel.append(val)
                numV = int(val[:-6])
        print('the name:',nameV)
        print('the num:',numV)
        edhChecker(nameV,numV)


def EdhChecker(data):
        try:
                c.execute('insert into EDHPOP values (?,?)',(
                getTime(),
                obj['prices']['usd']
                ))
        except:
                print('could not add to db')





