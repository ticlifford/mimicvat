
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

# this is a scraper for mtg deck lists that uses mtgtop8.com
# It takes a format URL as input
# It writes the decklist, sideboard, and deck information to a database file as output


#dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
#dbPath = 'G:/Documents/Misc/mimicvat_backup_db/CARDINFO.db'
dbPath = 'G:/Documents/coding files/mimicvat_db_2023/mini_db/CARDINFO.db'
#dbPath = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO.db'

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
uuid text primary key,
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

#open the meta time period dropdown on a format and run open_meta for each
def format_metas(url):
    print('running format_metas')
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    for x in soup.find_all('div',{'id':'metas_list'}):
        print('finding meta lists')
        #print('x:')
        #print(x)
        # i should be making a list of the 'a' tags and then running my open_meta loop after
        # garbage collection
        for y in x.find_all('a'):
            #print('y href: ',y['href'])
            #print('meta: ',y.string)
            #print("https://mtgtop8.com/format" + y['href'], y.string)
            open_meta("https://mtgtop8.com/format" + y['href'], y.string)
            break


# opens every 'next page' link on a format url
# produces a 'new url' for the next page

#open_meta finds the next page on a meta until there isn't a next page
#url is url for the selected dropdown
# meta is the string tag of that dropdown, something like "last 2 months" or "all 2017 decks"

def open_meta(url, meta):
    print('i am processing url in open_meta:',url)
    #print('the meta: ',meta)
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')

    #send url to explore_event
    try:
        print('processing events from meta page')
        explore_event(url, meta)
    except:
        print('could not process events from meta')

    #check if there's a next page and run recursion
    try:
        next_button = soup.find("a", string="Next")
        new_url = legacy_url[:-5] + next_button.get('href')
        print('the new_url:',new_url)

        print('starting up explore_event')
        # explore_event scrapes each event url from the page
        # then it calls event_processor
        print('running recursion')
        open_meta(new_url, meta)
    except:
        print('there is no next url')
    #collect the next and pass it to open_meta
    #open_meta(next_url)

# explore_event finds every event(and link) on the page, runs open_meta
#passes url, meta, and date to event_processor

def explore_event(event_url, meta):
    #import pdb; pdb.set_trace()
    url = event_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    try:
        #all_tables = soup.find_all('tr',class_='hover_tr')
        #last_events = soup.find_all('table',class_='Stable')[1]
        #selects the "last 20 events" table, which is the second on the page
        last_events = soup.find_all('table',class_='Stable')[1]
        #print('last_events',last_events)
        #s14 = last_events.find_all('td',class_='S14')
        #print(s14[0])
    except:
        print('could not find_all table')

    #create a list of the links for each deck in the table
    links = []
    try:
        rows = last_events.find_all('tr')
        for row in rows:
            cols = row.find_all('td')

            col_list = []
            for item in cols:
                col_list.append(item)
            a_href=col_list[1].a['href']
            col_date = col_list[3].text.strip()
            # add the event url and date to a list called links
            links.append([a_href,col_date])
    except:
        print('could not comprehend table')
    try:
        for event_data in links:
            try:
                print('starting event_processor for link')
                event_processor("https://mtgtop8.com/" + event_data[0],meta, event_data[1])
            except:
                None
        #print(links)

        """
        for atag in s14:
            #print("https://mtgtop8.com/" + atag.a['href'])
            links.append("https://mtgtop8.com/" + atag.a['href'])
            #implement deck scrape for that href
        for x in links:
            try:
                print('starting event_processor for ',x)
                event_processor(x, meta)
            except:
                None
        """
    except:
        print('failed to find, probably table comprehension issue')

# this scrapes the deck that's on the page
def deck_scrape(deck_scrape_url, meta, event_date, deck_name,place,player_name):
    url=deck_scrape_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    meta = meta
    #find the deck name, player name, date, event name
    #event is in class_="event_title" and its the first one. deck name is second
    event_title = soup.find_all(class_='event_title')
    #print('event title class results:')
    #for thing in event_title:
    #    print(thing.string)
    
    #generate uuid:
    deck_uuid = uuid.uuid1()
    print('deck_uuid: ', deck_uuid)
    #deck_name = event_title[1].find('a').previousSibling

    event_title = event_title[0].string
    print('event title: ',event_title)
    print('deck name: ',deck_name)
    print('player name: ',player_name)


    #deck_name
    #deck_uuid
    #event_date
    #event_title
    #player_name
    #meta

    try:
        print('place: ',place, 'meta: ',meta)
    except:
        print('could not print place or meta')
    #import pdb; pdb.set_trace()

    try:
        c.execute('insert or ignore into deck_meta values (?,?,?,?,?,?,?)',(
            str(event_title),
            str(event_date),
            str(player_name),
            str(meta),
            str(deck_uuid),
            str(deck_name),
            str(place),
        ))
    except:
        print('could not push deck_meta vals to sql')

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
                try:
                    c.execute('insert or ignore into side_board values (?,?,?)',(
                        str(deck_uuid),
                        str(slot[1]),
                        slot[0]
                    ))
                    side_board.append(slot)
                except:
                    print('could not push side_board to sql')
            else:
                #print('adding to main board')
                main_board.append(slot)
                # add to mainboard
                try:
                    c.execute('insert or ignore into main_deck values (?,?,?)',(
                        str(deck_uuid),
                        str(slot[1]),
                        slot[0]
                    ))
                except:
                    print('could not push main_deck to sql')

        print('main board: ',main_board)
        print('side board: ',side_board)

        #print(file_list)
        #this works except for accents in the file name

def add_mainboard():
    None

def add_sideboard():
    None

# event_processor receives a list of events, their meta, and their date
# checks the list of decks in the event
# it creates a link to that deck's page, finds player name
# it calls the deck scraper
def event_processor(event_url, meta, event_date):
    #count the number of decks in the sidebar
    url=event_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    hrefs = set()
    for x in soup.find_all('div',attrs={'style':'margin:0px 4px 0px 4px;'}):
        deck_line = x.find_all('div',attrs={'style':'padding:3px 0px 3px 0px;'})
        deck_list = []
        # deck_line is a list of decks pulled from the left hand sidebar
        # each 'y' is a deck listing with place, deck name, and player name
        for y in deck_line:
            #import pdb; pdb.set_trace()
            print('new y line')
            #this means new deck, first y is place and second is both name and link
            S14 = y.find_all('div',class_='S14')
            deck_name = S14[1].text
            print('deck_name; ',deck_name)
            p_name = y.find_all('div',class_='G11')[0].string
            print("player name: ",p_name)

            new_deck=[]
            for a in S14:
                print('a string:',a.string)
                # adding deck name to deck
                new_deck.append(a.string)
                link = a.find('a')
                if link:
                    print('found link')
                    #adding deck url to deck
                    new_deck.append(link['href'])
                
            deck_list.append(new_deck)
        print('deck list:')
        print(deck_list)
        for deck in deck_list:
            try:
                print('deck details:',deck)
            except:
                print('could not print deck details')
            try:
                print('meta and event date:',meta,event_date)
            except:
                print('could not print meta or event date')
            try:
                print('deckscraping')
                #print('url:',deck[2])
                #deck_scrape(deck_scrape_url, meta, event_date, deck_name,place)
                #import pdb; pdb.set_trace()
                deck_scrape("https://mtgtop8.com/event" + deck[2],meta,event_date, deck_name,deck[0],p_name)
            except:
                print('could not manage decklist')
                break


print('starting decklist scraper for legacy 2 weeks')
print('connecting to db')
cardsDb = sqlite3.connect(dbPath)
c = cardsDb.cursor()


#"""
last2weeks = "https://mtgtop8.com/format?f=LE&meta=34&a="
open_meta(last2weeks, "legacy")
#"""

cardsDb.commit()
print('im closing the db')
cardsDb.close()



# this script is mostly completed. You pass it a format link on mtgtop8, and need to hardcode the format.
# it also needs tuning up around the open_meta stuff. I think I still need to fix the ascii/utf-8 thing where accent marks crash the scraper
# it also needs to delay at the deck scraping thing


#last 2 weeks
#https://www.mtgtop8.com/format?f=LE&meta=34&cp=1


#open_meta("https://mtgtop8.com/format?f=LE&meta=34&a=","last 2 weeks")