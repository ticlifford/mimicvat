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
                (ID text primary key,
                PRICEDIRECTION text,
                UNIQUE(ID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS RESERVEDCHANGE
                (ID text primary key,
                CHANGE real,
                UNIQUE(ID))''')

#    c.execute('''CREATE INDEX RL_CHANGE_INDEX
#                ON RESERVEDCHANGE (ID)''')

    c.execute('''CREATE TABLE IF NOT EXISTS PRICECHANGE
                (ID text primary key,
                CHANGE real,
                UNIQUE(ID))''')

#    c.execute('''CREATE INDEX PRICE_CHANGE_INDEX
#                ON PRICECHANGE (ID)''')

    c.execute('''CREATE TABLE IF NOT EXISTS PRICES
                (ID text,
                DATETIME text,
                NORMPRICE real,
                FOILPRICE real,
                FOILRATIO real,
                PRIMARY KEY(ID,DATETIME))''')

    c.execute('''CREATE TABLE IF NOT EXISTS PRICETODAY
                (ID text,
                NORMPRICE real,
                FOILPRICE real,
                PRIMARY KEY(ID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS BUYLIST
                (NAME text,
                DATETIME text,
                SETNAME text,
                BUYPRICE real,
                PRIMARY KEY(NAME,SETNAME))''')

    c.execute('''CREATE TABLE IF NOT EXISTS CARDSET
                (NAME text,
                CODE text,
                RELEASEDATE text,
                PRIMARY KEY(CODE),
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
                RESERVED text,
                tcgplayer_id real,
                cardmarket_id real,
                boosterfun text,
                PRIMARY KEY(ID),
                UNIQUE(ID))''')

    c.execute('''CREATE TABLE IF NOT EXISTS FRONTPAGE
                (DATETIME text,
                NORMPRICE real,
                PRIMARY KEY(DATETIME),
                UNIQUE(DATETIME))''')

    c.execute('''CREATE TABLE IF NOT EXISTS COLLECTIONS
                (USER_ID text,
                CARD_ID text,
                COST_PAID real,
                MSRP real,
                NUMBER_OWNED real,
                NAME text,
                CODE text,
                DATETIME text,
                transaction_id integer primary key autoincrement,
                unique(transaction_id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS COLLECTION_VAL
                (USER_ID text,
                COL_VAL real,
                PAID_VAL real,
                DATETIME text,
                UNIQUE(DATETIME),
                PRIMARY KEY (USER_ID, DATETIME)
                )''')
    cardsDb.close()

    print('database was created')
except:
    print('database could not be created')