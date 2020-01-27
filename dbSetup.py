import sqlite3

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

#cards: ID, NAME, CMC, COLOR, SET, PICTURE 
#prices: ID, PRICE, FOILPRICE, DATE
#edhpop: ID, EDHNUM
#watchlist:
#cardset:
#buylist:

# my databases link with the unique key called ID, which represents each unique card
# these are generated/provided by the scryfall API which I scrape

try:
    c.execute('''CREATE TABLE IF NOT EXISTS EDHPOP
                (NAME text,
                EDHNUM real)''')

    c.execute('''CREATE TABLE IF NOT EXISTS WATCHLIST
                (ID text,
                PRICEDIRECTION text,
                UNIQUE(ID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS PRICES
                (ID text,
                DATETIME text,
                NORMPRICE real,
                FOILPRICE real,
                FOILRATIO real)''')

    c.execute('''CREATE TABLE IF NOT EXISTS BUYLIST
                (NAME text,
                DATETIME text,
                SETNAME text,
                BUYPRICE real)''')

    c.execute('''CREATE TABLE IF NOT EXISTS CARDSET
                (NAME text,
                CODE text,
                RELEASEDATE text,
                UNIQUE(CODE))''')

    c.execute('''CREATE TABLE IF NOT EXISTS CARDS
                (ID text,
                NAME text,
                CMC real,
                MANACOST text,
                POWER text,

                TOUGHNESS text,
                COLOR text,
                CARDSET text,
                TYPE text,
                PICURL text,

                FOIL text,
                NONFOIL text,
                ONLINEONLY text,
                RARITY text,
                UNIQUE(ID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS FRONTPAGE
                (DATETIME text,
                NORMPRICE real,
                UNIQUE(DATETIME))
                ''')

    print('database was created')
except:
    print('database could not be created')