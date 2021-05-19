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
def fetch_rm():
    print('fetching rares and mythics list')
    cList = []
    try:
        # fill cList with all mythics and rares
        # I'm formatted to convert it to card kingdom's csv format

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
    return cList
cList = fetch_rm()

cardsDb.close()


def selectRows(cList):
    # converts cList into 500 long chunks, then returns that chunk as popList and passes it to pasteHtml
    # This calls pasteHtml with broken chunks of the rares and mythics from cList. cardkingdom takes 500 cards max,
    # so it divides the list into chunks to process it.
    while len(cList) != 0:
        print('clist is not zero')
        popList = []
        # for i in range(0,500):
        # I think i'm testing it with 20
        for i in range(0, 20):
            if len(cList) == 0:
                # this means the cList is empty, everything has been pop'd
                print('breaking popList append')
                break
            else:
                popList.append(cList.pop(0))
                print('appending popList')
        print('range loop finished, poplist length should be 20 or less')
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

    # htmlId is the ID value of the tag that I'm looking to paste into
    # here, I fill the html text box with my pasteVal, then hit the submit button
    htmlId = r"csvPaste"
    pasteBox = browser.find_by_id(htmlId)
    pasteBox.fill(pasteVal)

    submitId = r"convertPastedCsv"
    submit = browser.find_by_id(submitId).first.click()


selectRows(cList)

# here is where I left off. I haven't collected the values of each card yet.
# I only post.

# the next step is using beautiful soup to collect the values from cardkingdom,
# adding them to a dictionary, then inserting them to two new sql tables.
# one will contain historical buylist values for cards, the second will contain only today's value
# this will make searching for the day's value snappy in the browser,
# # while also maintaining historical data for charting

# beautiful soup scrape
# the values I am scraping are at <li class="result">
# span class="dName" is the card name
# span class="dPrice" is the ck buylist price
# li class="eidtionName" is the edition name

# card kingdom divides the cards by their set in editionwrapper so:
# for each edition wrapper, select the editionName
# then for each result in that edition wrapper, append the return list with name, ck_price, editionName