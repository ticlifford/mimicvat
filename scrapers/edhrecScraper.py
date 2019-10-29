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


#i'm going to swap out 'c18' for each set, there are about 30 of them


#functions: 
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

#print(html)
soup = b(html, 'html.parser')

s=soup.find('script')
#print(s)

#there are a handful of script tags, and I want a certain one
#then I cut out some of the string to get it in dic format
scripts = soup.find_all('script')
dic = scripts[-3]
dic = str(dic)
cardDic = dic[26:-10]

cardDic = json.loads(cardDic)
oGdic = cardDic
cardDic = cardDic['cardlists']
#print('the len of cardDic cardlists:',len(cardDic))



cardDic = cardDic[0]

cardDic = cardDic['cardviews']
#print(type(cardDic))
#print(len(cardDic))

#access db
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


<<<<<<< HEAD:final/scrapers/edhrecScraper.py
#close db
cardsDb.commit()
print('im closing the db')
cardsDb.close()
=======
def EdhChecker(data):
        try:
                c.execute('insert into EDHPOP values (?,?)',(
                getTime(),
                obj['prices']['usd']
                ))
        except:
                print('could not add to db')


>>>>>>> 99a6458680a33e5a511415f21ff5dc8b1917cf21:final/edhrecScraper.py

"""
#there's probably an easier way to do this
with open('edh.csv','w') as csvfile:
    for x in range(0,len(cardName)-1):
        csvfile.write(cardName[x])
        csvfile.write(',')
        csvfile.write(cardLabel[x])
        csvfile.write('\n')
"""


