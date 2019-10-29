#
#
# this is a work-in-progress to scrape mtggoldfish posted tournament decks
#
# it currently prints html stuff for the tournies, I think
#


import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import sqlite3

addCards = {}

def getTourny():
    url = 'https://www.mtggoldfish.com/metagame/standard#paper'
    html = urllib.request.urlopen(url).read()
    #print('the type of html:',type(html))
    soup = b(html, 'html.parser')
    hTag = soup.find_all('h4')
    
    tournyList = []
    for x in hTag:
        tournyList.append(x)
        #print(x.text)
    """
    print('first:')
    print(hTag[2])
    print('last:')
    print(hTag[-10])
    """
    print('tournyList list object')
    for i in range(2,len(tournyList)-10):
        print(tournyList[i].find_all('a'))
        #print()

    """
    soup = b(hTag, 'html.parser')
    for x in soup.find_all('a'):
        print(x)
    """

def getDeckUrl(url):
    #insert the URL for the mtggoldfish events page
    #this function scrapes the ending tag url that links to the deck list (currently just tournament-decklist-odd, needs to do even(t) too)
    #also currently only scrapes the first deck

    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')

    #find all decks in this list
    decks = soup.find_all('tr', {'class' : 'tournament-decklist-odd'})

    #print('the len:',len(decks))
    #for each deck in the list 
    count = 0

    #for every deck in on the page labeled odd, increase the count, and run getDeckCards for it's url
    for deck in decks:
        #print ('the deck is:',deck)
        count = count + 1
        #print('current count:',count)
    #deck = decks[0]
        deckURL = deck.find_all('td')
        #print("deckurl 1:",deckURL[1])
        deckURL = deckURL[1]

        #gets the URL ending for the deck
        for URL in deckURL.find_all(href = True):
            #return URL['href']
            print('running getdeckcards for url:',URL['href'])
            getDeckCards(URL['href'])
    #print('final count:',count)

    decks = soup.find_all('tr', {'class' : 'tournament-decklist-event'})
    
    #print('the len:',len(decks))
    #for each deck in the list 
    count = 0

    #for every deck in on the page labeled odd, increase the count, and run getDeckCards for it's url
    for deck in decks:
        #print ('the deck is:',deck)
        count = count + 1
        #print('current count:',count)
    #deck = decks[0]
        deckURL = deck.find_all('td')
        #print("deckurl 1:",deckURL[1])
        deckURL = deckURL[1]

        #gets the URL ending for the deck
        for URL in deckURL.find_all(href = True):
            #return URL['href']
            print('running getdeckcards for url:',URL['href'])
            getDeckCards(URL['href'])
    #print('final count:',count)







def getDeckCards(backUrl):
    frontUrl = "https://www.mtggoldfish.com"
    url = frontUrl + backUrl
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')

    cards = soup.find_all('td', {'class' : 'deck-col-card'})
    #print(cards)
    cardList = []
    for card in cards:
        cardList.append(card.text[1:-1])
        #print('the card:',card.text)
    #print(cardList)

    cards = soup.find_all('td', {'class' : 'deck-col-qty'})
    #print(cards)
    cardQty = []
    for card in cards:
        cardQty.append(card.text[1:-1])
        #print('the card:',card.text)
    #print(cardQty)
    cardDic = {}
    for x in range(len(cardList)):
        cardDic[cardList[x]] = int(cardQty[x])
    #print(cardDic)
    for key, val in cardDic.items():
        if key not in addCards:
            addCards[key] = val
        else:
            addCards[key] = addCards[key] + val
    
    
    #return cardDic

#def updateDb(cardDic):



#curl = getDeckUrl('https://www.mtggoldfish.com/tournament/fandom-legends-may-9-2019#paper')
#getDeckCards(curl)

"""

getDeckUrl('https://www.mtggoldfish.com/tournament/fandom-legends-may-9-2019#paper')

for key, val in addCards.items():
    print('the key:',key,'the value:', val)

"""

getTourny()