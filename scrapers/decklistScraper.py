
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
#from wget

#beautiful soup scraper to insert lists into db

#create three tables:
#1
#deck metadata
#eventname
#date
#username
#format
#uniqueID
#deckname
#record

#2 mainboard
#uniqueID
#cardname
#quantity

#3 sideboard
#uniqueID
#cardname
#quantity

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

def event_scrape(event_scrape_url):
    url=event_scrape_url
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    for x in soup.find_all(string=re.compile('Expor')):
        txt_file = x.parent.a['href']
        txt_url = "https://mtgtop8.com/" + txt_file
        print('scraping ',txt_url)
        data = urllib.request.urlopen(txt_url.encode('utf-8'))
        for line in data:
            print(line)
        #this works except for accents in the file name



#open_event(legacy_url)
#explore_event(legacy_url)
leg_event = 'https://mtgtop8.com/event?e=32512&f=LE'
event_scrape(leg_event)