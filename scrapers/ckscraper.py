from splinter import Browser
import sqlite3
import urllib.request
from bs4 import BeautifulSoup as b


# sets up an html soup parser for some URL
# this is probably for collecting the data after the post,
# and I haven't finished it

#card kingdom's bulk importer works with card names and sets.
#pass a list of names and sets to selectRows(cList)
#note, this script uses a chrome driver file for the automation and its currently linked to the desktop of my computer

# configure scraper and db connection
"""
html = urllib.request.urlopen(url).read()
soup = b(html, 'html.parser')
"""

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

# SQL search for all mythics and rares, and outputs them in a list called cList
cList = []
try:
    # fill cList with all mythics and rares

    for x in c.execute('select name, cardset from cards where rarity = "mythic"'):
        innerList = '"'+x[0]+'",'+x[1]+',0,1 \n'
        cList.append(innerList)
except:
    print('could not write sql function')

# posts each card after list creation
"""
for x in cList:
    print(x)
"""

cardsDb.close()


def selectRows(cList):
    # converts cList into 500 long chunks, then returns that chunk as popList and passes it to pasteHtml
    while len(cList) != 0:
        print('clist is not zero')
        popList = []
        # for i in range(0,500):
        for i in range(0, 20):
            if len(cList) == 0:
                # this means the cList is empty, everything has been pop'd
                print('breaking popList append')
                break
            else:
                popList.append(cList.pop(0))
                print('appending popList')
        print('range loop finished, poplist length should be 20')
        print('poplist len:', len(popList))
        # the loop counts up items and finishes here. I should call the function to run the chrome sim here
        pasteHtml(popList)
        # print(popList)
        #pasteVal = popList
        # return pasteVal
    print('clist is at zero')


def pasteHtml(popList):
    # starts the chrome environment, creates the pasteVal with popList, passes it to the browser and submits

    executable_path = {
        'executable_path': r'C:\Users\Tim\Desktop\chrome\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(r"https://www.cardkingdom.com/static/csvImport")
    pasteVal = ''

    for x in popList:
        pasteVal = pasteVal + x

    # htmlId is, naturally, the ID value of the tag that I'm looking to paste into
    # here, I fill the html text box with my pasteVal, then hit the submit button
    htmlId = r"csvPaste"
    pasteBox = browser.find_by_id(htmlId)
    pasteBox.fill(pasteVal)

    submitId = r"convertPastedCsv"
    submit = browser.find_by_id(submitId).first.click()


selectRows(cList)

# here is where I left off. I haven't collected the values of each card yet.
# I only post.
