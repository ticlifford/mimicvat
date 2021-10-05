
import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib import parse
import csv
import datetime
import time
import re
import uuid
import sqlite3


#dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO.db'

#from wget

#beautiful soup scraper to insert lists into db

#create three tables:
#1 : deck metadata
#eventname
#date
#username
#format
#uniqueID(key)
#deckname
#record
"""
create table if not exists deck_meta 
(eventname text,
eventdate text,
playername text,
format text,
uuid text,
deckname text,
place text);
"""


#2 mainboard
#uniqueID(key)
#cardname
#quantity

"""
create table if not exists main_deck 
(uuid text,
cardname text,
quantity real);
"""

#3 sideboard
#uniqueID(key)
#cardname
#quantity

"""
create table if not exists side_board 
(uuid text,
cardname text,
quantity real);
"""

#indexes
"""
create index maindeck_name on main_deck(cardname);
create index maindeck_uuid on main_deck(uuid);
create index sideboard_uuid on side_board(uuid);
create index sideboard_name on side_board(cardname);
"""
#scraper

#legacy decks from top8
legacy_url = "https://mtgtop8.com/format?f=LE"

#html = urllib.request.urlopen(url).read()
#soup = b(html, 'html.parser')

#results=soup.find_all("div",class_="S14")
"""
for job_el in results:
    #these are links to events
    #scrape each url
    print(job_el)
"""

def open_event(url):
    print('i am processing url:',url)
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    #scan all the events

    #check if there's a next
    try:
        next_button = soup.find("a", string="Next")
        new_url = legacy_url[:-5] + next_button.get('href')
        print('the new_url:',new_url)
        print('there is a next url:',new_url)
        print('running recursion')
        open_event(new_url)
    except:
        print('there is no next url')
    #collect the next and pass it to open_event
    #open_event(next_url)

def explore_event(event_url):
    url = event_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    try:
        #all_tables = soup.find_all('tr',class_='hover_tr')
        last_events = soup.find_all('table',class_='Stable')[1]
        s14 = last_events.find_all('td',class_='S14')
        #print(s14[0])
        for atag in s14:
            print(atag.a['href'])
            #implement deck scrape for that href
    except:
        print('failed to find')

#more of a deck scraper than event scraper
def event_scrape(event_scrape_url):
    url=event_scrape_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')

    #find the deck name, player name, date, event name
    #event is in class_="event_title" and its the first one. deck name is second
    event_title = soup.find_all(class_='event_title')
    #print('event title class results:')
    #for thing in event_title:
    #    print(thing.string)
    
    #generate uuid:
    deck_uuid = uuid.uuid1()
    print('deck_uuid: ', deck_uuid)
    deck_name = event_title[1].find('a').previousSibling

    event_title = event_title[0].string
    print('event title: ',event_title)
    print('deck name: ',deck_name)
    #player name is in class_="player_big"
    name = soup.find_all(class_='player_big')
    player_name = name[0].string
    print('name: ',player_name)

    event_date = soup.find(class_='meta_arch')
    print('event_date: ',event_date)

    #deck_name
    #deck_uuid
    #event_date
    #event_title
    #player_name
    c.execute('insert into deck_meta values (?,?,?,?,?,?,?)',(
        str(event_title),
        #event_date,
        'date',
        str(player_name),
        'legacy',
        str(deck_uuid),
        str(deck_name),
        'place'
    ))

    # finds the txt file for the decklist
    for x in soup.find_all(string=re.compile('Expor')):
        txt_file = x.parent.a['href']
        txt_url = "https://mtgtop8.com/" + txt_file
        print('scraping ',txt_url)
        data = urllib.request.urlopen(txt_url)
        file_list = []
        for line in data:
            dec_line = line.decode('UTF-8')
            file_list.append(dec_line[:-2].split(" ",1))
            #print(line)
        
        sb = 0
        main_board = []
        side_board = []
        for slot in file_list:
            #print('processing slot: ',slot)
            if slot[0] == 'Sideboard':
                sb = 1
                #print('found sideboard')
            elif sb is 1:
                # add to sideboard
                #print('adding to side board')
                c.execute('insert into side_board values (?,?,?)',(
                    str(deck_uuid),
                    str(slot[1]),
                    slot[0]
                ))
                side_board.append(slot)
            else:
                #print('adding to main board')
                main_board.append(slot)
                # add to mainboard
                c.execute('insert into main_deck values (?,?,?)',(
                    str(deck_uuid),
                    str(slot[1]),
                    slot[0]
                ))
        print('main board: ',main_board)
        print('side board: ',side_board)

        #print(file_list)
        #this works except for accents in the file name

def add_mainboard():
    None

def add_sideboard():
    None

def event_processor(event_url):
    #count the number of decks in the sidebar
    url=event_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    hrefs = set()
    for x in soup.find_all('div',attrs={'style':'margin:0px 4px 0px 4px;'}):
        ats = x.find_all('a', href = True, class_=None,attrs={"src":False})
        for y in ats:
            print(y)
            print(y.get('href'))
            if y.get('href') != '':
                hrefs.add(y.get('href'))
    
    #a set of deck urls to process
    print('set: ',hrefs)

#open_event(legacy_url)
#explore_event(legacy_url)
leg_event = 'https://mtgtop8.com/event?e=32512&f=LE'
#event_processor(leg_event)
#event_scrape(leg_event)



print('connecting to db')
cardsDb = sqlite3.connect(dbPath)
c = cardsDb.cursor()


event_scrape(leg_event)

cardsDb.commit()
print('im closing the db')
cardsDb.close()