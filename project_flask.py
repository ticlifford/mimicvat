from urllib.parse import _NetlocResultMixinBase
from flask import Flask, render_template, request
import sqlite3 as sql
import cardAverage
#import db_location
from db_location import dbLoc
import dbSetup
import os
import datetime
import time
from flask_paginate import Pagination, get_page_parameter, get_page_args

#from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#from flask_login import LoginManager
#login_manager = LoginManager()
"""


# This is my flask file which runs the application

app = Flask(__name__)

# the location of the database, when running locally vs on server

#website location

#i'm intending to search for the db, and create it with dbsetup if it isn't
#i should then run weekly, then daily
"""
if os.path.isfile('CARDINFO.db'):
    print('found db')
    None
else:
    print('did not find db, creating now')
"""

#dbLoc = 'CARDINFO.db'

#windows local
#dbLoc = 'G:/Documents/coding files/mimicvat_db_2023/CARDINFO.db'


#csv file upload location
UPLOAD_FOLDER = 'static/files'


try:
    print('collecting distinct names')
    card_names = []
    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('''select distinct(name) 
    from CARDS 
    where substr(type,1,5) != "Token" 
    and substr(type,1,6) != "Emblem" 
    and substr(type,1,4) != "Card" 
    and substr(type,1,6) != "Scheme" 
    and onlineonly = "False" 
    and nonfoil = "True"''')
    rows = cur.fetchall()
    con.close()
    for x in rows:
        card_names.append(x[0])
except:
    print('could not collect distinct names')
#
# App routes:
#
# index: the front page, I have a static card example to show the site's features
# list: I fetch and display a set of cards so users can see what kind of data I have
# watchlist: a list of cards users can modify to track cards with
# search: a series of get/post routes for searching for specific cards
# topcards: an experimental page for displaying useful statistics and potential future features.
# I have it displaying some pandas stuff right now.


@app.route('/')
def index(chartID='chart_ID', chart_type='line', chart_height=500):
    # the front page with a static example card
    priceList = []
    foilList = []
    dateList = []
    cardId = "810a3792-a689-4849-bc14-fb3c71153aba"
    imageUrl = ""
    cardName = "Land Tax"

    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()

    imageUrl = 'https://img.scryfall.com/cards/normal/front/8/1/810a3792-a689-4849-bc14-fb3c71153aba.jpg?1562920975'


    # collects price and date vals of land tax to load up front page quickly
    try:
        imageUrl = searchCard(cardId, cur, priceList, foilList, dateList, imageUrl, False)
        data = [list(x) for x in zip(dateList, priceList)]
    except:
        print('could not connect to db for frontpage chart')
    con.close()
    try:
        print(data)
        print('printing data')
    except:
        print('could not print data')
    """
    # chart insertion
    try:
        # 7 day SMA
        window_size = 30
        numbers = priceList
        i = 0
        moving_averages = []
        while i < len(numbers) - window_size + 1:
            this_window = numbers[i : i + window_size]

            window_average = sum(this_window) / window_size
            moving_averages.append(window_average)
            i += 1
        print(moving_averages)
        for x in range(0,window_size-1):
            moving_averages.insert(x,priceList[x])
        smadata = [list(x) for x in zip(dateList, moving_averages)]


    except:
        print('sma failed')
    """
    try:
        chart = {"renderTo": chartID, "type": chart_type,
        "height": chart_height, "zoomType": 'x', "backgroundColor":"#f5f5f5"}
        series = [{"name": 'series label', "data": data}]

        title = {"text": cardName}
        xAxis = {"type":"datetime"}
        yAxis = {"title": {"text": ''}}
        pageType = 'graph'


    except:
        print('something went wrong with the highcart vars')

    return render_template('frontPage.html',
                           pageType=pageType,
                           chartID=chartID,
                           chart=chart,
                           series=series,
                           title=title,
                           xAxis=xAxis,
                           yAxis=yAxis,
                           imageUrl=imageUrl,
                           cardId=cardId,
                           cardName=cardName,
                           card_names=card_names)

@app.route('/collections')
def collectionsPage():
    return render_template("yourCollection.html", card_names = card_names)
    """
    try:
        print('hello collection page')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from collections")
        rows = cur.fetchall()
        con.close()
        colls = rows
    except:
        print('hello collections page is not working')
    """
"""
@app.route('/collections/<collection_id>', methods = ['GET', 'POST'])
def collectionsPage():
    try:
        print('hello collection page')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from collections")
        rows = cur.fetchall()
        con.close()
        colls = rows
    except:
        print('hello collections page is not working')

# the collections sql table will look like this:
#   *COLLECTION_ID    CARD_ID    QUANTITY
#the second sql table will be collections metadata:
#   USERNAME    COLLECTION_VAL   *COLLECTION_ID    COLLECTION_NAME

#   the unique keys of the database will both be Collection_ID
#   usernames can have more than one collection

    return render_template("collections.html", card_names = card_names)
"""
@app.route('/sets')
def setsPage():
    try:
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select name, code, releasedate from cardset where substr(name,-6,6) != 'Tokens' and substr(name,-6,6) != 'Promos' and substr(name,-9,9) != 'Oversized' order by releasedate desc")
        rows = cur.fetchall()
        con.close()
        setnames = rows
    except:
        print('could not collect set data')
        setnames = []
    return render_template("sets.html", setnames = setnames,card_names=card_names)

@app.route('/testfilter')
def testfilter():
    return render_template('testfilter.html')

@app.route('/setinfo/<setid>', methods=['GET', 'POST'])
def setinfo(setid):
    try:
        #db connection
        print('connecting to db')
        con = sql.connect(dbLoc)
        #con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db in setinfo')

    try:
        #set name collection
        print('selecting name for ',setid)
        setname = cur.execute('select name from CARDSET where code = ?', (setid,))
        setname = setname.fetchone()[0]
        fullsetname = setname
        setname = str(setname).lower().replace(" ", "")
    except:
        print('could not select cardset name')

    try:
        #set size
        print('counting set size')
        numcards = cur.execute('select count(name) from cards where cardset = ?', (setid,))
        numcards = numcards.fetchone()[0]
    except:
        print('could not count numcards')

    try:
        # this crashes the page because i don't even have a pricetoday table

        # cards collection, selects recent date, fetches recent_date
        setcards = cur.execute('select cards.id, name, picurl, pricetoday.normprice, cards.rarity, pricetoday.foilprice from cards, pricetoday where cardset = ? and cards.id=pricetoday.id order by pricetoday.normprice desc', (setid,))
        return_list = []
        for card in setcards:

            return_list.append(list(card))
        #recent_date = cur.execute('select max(datetime) from prices')
        #recent_date = recent_date.fetchone()[0]
        #print('recent date:',recent_date)
    except:
        print('couldnt finish recent_date stuff')


    #return render_template('setinfo.html',setnorm = setnorm,setfoil=setfoil,ratio=ratio,setcode=setid,carddeck = setcards)
    return render_template('setinfoold.html',setcode=setid, carddeck = return_list,card_names=card_names, setname=setname,fullsetname=fullsetname,numcards=numcards)

@app.route('/change')
def change():

    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db')

    try:
        cur.execute('''select cards.name, PRICECHANGE.change, cards.cardset, cards.id, cards.picurl, pricetoday.normprice 
        from cards, PRICECHANGE, PRICETODAY 
        where cards.onlineonly = FALSE and cards.id = pricetoday.id and cards.cardset not in ('cei','wc99') and length(cards.cardset)<4 and cards.ID=PRICECHANGE.id 
        order by PRICECHANGE.change desc limit 10''')

        top_10 = cur.fetchall()
        top_10_list = []
        for x in top_10:
            top_10_list.append([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
            print([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
        top_10 = top_10_list
    except:
        print('could not get top 10 rl')

    try:
        cur.execute('''select cards.name, PRICECHANGE.change, cards.cardset, cards.id, cards.picurl 
        from cards, PRICECHANGE, PRICETODAY 
        where cards.onlineonly = FALSE and cards.cardset not in ('cei','wc99') and length(cards.cardset)<4 and cards.ID=PRICECHANGE.id 
        order by PRICECHANGE.change asc limit 10''')

        bot_10 = cur.fetchall()
        bot_10_list = []
        for x in bot_10:
            bot_10_list.append([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
            print([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
        bot_10 = bot_10_list
    except:
        print('could not get bot 10 rl')
    con.close()
    return render_template('changeList.html',
                        top_10 = top_10,
                        bot_10 = bot_10,
                        card_names=card_names
                        )


@app.route('/decks')
def decks():
    try:
        print("accessing decks")
    except:
        print('could not access decks')
    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()

    except:
        print('could not connect to db')
    try:
        cur.execute('select * from deck_meta;')
        deck_meta = cur.fetchall()
        #print(deck_meta)
        deck_list = []
        for row in deck_meta:
            row_data = []
            for line in row:
                row_data.append(line)
            deck_list.append(row_data)
        #deck_list.sort(key=lambda x: x[1])
        #print(deck_list)
        
        #for row in deck_meta:
        #    deck_list.append(row)
        #print("deck list:",deck_list)

    except:
        print('something went wrong')
    try:
        for row in deck_list:
            #import pdb; pdb.set_trace()
            row[1] = datetime.datetime.strptime(row[1], '%d/%m/%y').date()
            #print(row[1])
        deck_list.sort(reverse=True, key=lambda x: x[1])
        
    except:
        print('date time issue')
    try:
        #page = request.args.get(get_page_parameter(), type=int, default=1)
        page, per_page, offset = get_page_args(page_parameter="page",per_page_parameter="per_page")
        search = False
        q = request.args.get('q')
        if q:
            search = True
    except:
        print('no page pagination')

    try:
        def get_users(offset=0,per_page = 20):
            return deck_list[offset: offset+per_page]

        deck_list_total = len(deck_list)
        pagination_users = get_users(offset=offset,per_page = per_page)
    except:
        None




    try:
        #pagination = Pagination(page = page, total = len(deck_list), search = search, per_page = 20, record_name = "deck_list")
        pagination = Pagination(page = page, total = deck_list_total, per_page = per_page)
    except:
        print('pagination error')
    try:
        return render_template('decks.html',card_names=card_names,deck_list=deck_list, pagination=pagination,page=page,per_page=per_page,users=pagination_users)
    except:
        print('decks.html issue')
        return render_template('frontPage.html',card_names=card_names)

@app.route('/decks/<deck_uuid>')
def decksuuid(deck_uuid):
    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db')

    """
    try:
        cur.execute('select * from main_deck where main_deck.uuid= ?;',(deck_uuid,))
        deckList = cur.fetchall()
    except:
        print('could not fetchall main_deck')
    """
    try:
        cur.execute('''select distinct cards.PICURL, main_deck.cardname, cards.id, main_deck.quantity from main_deck, cards where 
        cards.NAME=main_deck.cardname and main_deck.uuid = ? group by main_deck.cardname;''',
        (deck_uuid,))
        deckList = cur.fetchall()
    except:
        print('could not fetchall main_deck')
#select distinct cards.PICURL, main_deck.cardname from main_deck, cards where cards.NAME=main_deck.cardname
# and main_deck.uuid = 'c1434c50-bebb-11ec-af4a-d8cb8a71a1eb' group by main_deck.cardname;

    try:
        return render_template('deckList.html',card_names=card_names,deckList=deckList)
    except:
        print('deckList.html issue')
        return render_template('frontPage.html',card_names=card_names)

@app.route('/monthly')
def monthlyMovers():

    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db')

    try:
        cur.execute('select name, cards.picurl, pricetoday.normprice, pricechange.change, cards.id from cards, pricechange, pricetoday where cards.id=pricetoday.id and cards.id=pricechange.id and pricetoday.normprice>1.00 order by pricechange.change desc limit 10;')
        top_10_sql = cur.fetchall()
        top_10 = []
        for x in top_10_sql:
            top_10.append([x[1],x[0],x[3],x[4]])
        return render_template('monthlyMovers.html',card_names=card_names,top_10=top_10)
    except:
        print('could not complete monthly')
        return render_template('frontpage.html',card_names=card_names)
@app.route('/reserveList')
def reserveList(chartID='chart_ID', chart_type='line', chart_height=500):
    # select all from reserve list sql table
    # reserve list sql table must be updated daily after price collection


    priceList = []
    dateList = []
    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db')


    try:
        print('run select query')
        cur.execute("select * from reservedhistory order by datetime asc")
        reserved_vals = cur.fetchall()
    except:
        print('could not select')

    try:
        today_date = cur.execute("select max(datetime) from prices")
        today_date  = cur.fetchone()
        #print("today_date ",today_date[0])
    except:
        print('could not process moving average')

    try:
        print('reserved_vals:')
        print(reserved_vals[0])
    except:
        print('could not print reserved_vals')

    try:

        print('appending chart lists')
        for vals in reserved_vals:
            print('vals:',vals[1],vals[0])
            priceList.append(vals[1])

            newdate = vals[0].replace("-","/")
            time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
            timestamp = datetime.datetime.timestamp(time_element)
            timestamp = int(timestamp)
            timestamp = timestamp*1000
            print('timestamp:',timestamp)
            dateList.append(timestamp)
        data = [list(x) for x in zip(dateList, priceList)]
        print('data: ',data)
    except:
        print('could not append chart lists')


    try:

        newdate = today_date[0].replace("-","/")
        print('today_date replaced:',newdate)


    except:
        print('could not do last_week 1')
    try:
        time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
        print('time element:',time_element.date())
        last_week = time_element - datetime.timedelta(days=7)
        todays_date = time_element
        print('todays_date',todays_date)
        yesterday_date = time_element - datetime.timedelta(days = 1)
        last_week = last_week.date()
        print('last week: ',last_week)
    except:
        print('could not do last week 2')
    try:
        cur.execute("select cards.name, RESERVEDCHANGE.change, cards.cardset, cards.id, cards.picurl from cards, RESERVEDCHANGE where cards.cardset not in ('cei','wc99','30a','ced') and length(cards.cardset)<4 and cards.ID=RESERVEDCHANGE.id order by RESERVEDCHANGE.change desc limit 10")
        top_10 = cur.fetchall()
        top_10_list = []
        for x in top_10:
            top_10_list.append([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
            print([x[0],"{0:.0%}".format(x[1]-1),x[2],x[3],x[4]])
        top_10 = top_10_list
    except:
        print('could not get top 10 rl')

    #cards collection
    try:
        print('run select query for cards')
        #I need to select a date so right now i have it subquerying the most recent, that will be too slow on the live app but fine locally
        #cur.execute("select prices.normprice,prices.id from cards, prices where cards.id=prices.id and reserved='True' and datetime='2021-04-21' order by normprice desc limit 10")
        #date_today = cur.execute("select max(datetime) from prices where id=")
        cur.execute("select prices.normprice,prices.id,cards.picurl from cards, prices where cards.id=prices.id and reserved='True' and datetime=(select max(datetime) from prices) order by normprice desc limit 3")
        rows = cur.fetchall()
        reserve_cards = rows

        for x in reserve_cards:
            None
    except:
        print('could not select reserve_top')


    con.close()

    # chart insertion
    try:
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x', "backgroundColor":"#f5f5f5"}
    except:
        print('chart cant be made')
    try:
        series = [{"name": 'series label', "data": data}]
    except:
        print('series cant be made')
    try:
        title = {"text": 'Total value of reserved list'}
        xAxis = {"type":"datetime"}
        yAxis = {"title": {"text": 'dollars'}}
        pageType = 'graph'
    except:
        print('something went wrong with the highcart vars')


    return render_template('reserveList.html',
                        pageType=pageType,
                        chartID=chartID,
                        chart=chart,
                        series=series,
                        title=title,
                        xAxis=xAxis,
                        yAxis=yAxis,
                        card_names=card_names,
                        reserve_cards=reserve_cards,
                        top_10 = top_10
                        )

@app.route('/list')
def listPage():
    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from CARDS where cardset='aer'")
    rows = cur.fetchall()
    con.close()

    return render_template("listLayout.html", rows=rows, card_names=card_names)

@app.route('/watchlist', methods=['POST', 'GET'])
def watchlist():

    if request.method == 'GET':
        print('watchlist get request')
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows, card_names=card_names)

    # post to insert
    elif request.form.get('removeCard') == None:
        print('/watchlist post request insert')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        # this is the name from html
        r = (request.form['watchlist'])

        cardId = ""
        valueIndicator = ""

        # card ID fetching
        # selects first available ID where id's len is 3
        try:
            for cardIdNum in cur.execute("""select ID 
            from CARDS 
            where UPPER(NAME)=UPPER((?)) 
            and cards.ONLINEONLY != 'True' 
            and length(cardset)=3 
            and nonfoil = 'True'""",
                                         (r, )):
                cardId = cardIdNum[0]
        except:
            print('could not find card')

        # the cardAverage week/month for the searched card
        valueIndicator = cardAverage.weekMonth(cardId)[2]

        # insert to watchlist
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)",
                        (cardId, valueIndicator, ))
            con.commit()
        except:
            print('could not insert card')
        con.close()

        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows, card_names=card_names)

    # post request to remove card from list
    else:
        print("remove card post request")
        con = sql.connect(dbLoc)
        cur = con.cursor()
        cardID = request.form.get('removeCard')

        try:
            cur.execute("delete from watchlist where ID=(?)", (cardID, ))
            print('removed ', cardID, ' from watchlist')
        except:
            print('could not remove card from watchlist')
        con.commit()
        con.close()

        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows, card_names=card_names)




@app.route('/search/<cardId>', methods=['GET', 'POST'])
def searchID(cardId, chartID='chart_ID2', chart_type='line', chart_height=500):
    # the search bar results for the layout html
    
    if request.method == "GET":
        print('search cardID get request')
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()

        # initializing my variables
        priceList = []
        foilList = []
        dateList = []
        imageUrl = ""
        sameCards = []
        setCodes = []
        duplicate_names = []
        cardInfo = {}
        cardName = ""

        # selects name and set of the card
        try:
            for x in cur.execute("select NAME, CARDSET, NONFOIL from CARDS where ID=(?)", (cardId, )):
                #print('the name is:', x[0])
                #print('the set is:', x[1])
                cardName = x[0]
                setCodes.append(x[1])
                # does a nonfoil version exist?
                nonfoil = x[2]
            print('a nonfoil exists:',nonfoil)
        except:
            print('I couldnt get the card name')

        try:
            price_now = recent_price(cardId)
            print('fetching price_now')
        except:
            print('could not get price today')

        # select ids of all reprints
        print('card im looking up:', cardId)
        try:
            # creating duplicates list to display other versions
            for x in cur.execute("""select id, 
            cardset, 
            picurl
            from cards 
            where name = (?) 
            and cards.ONLINEONLY != 'True'""", (cardName,)):
                try:
                    sameCards.append(x[0])
                except:
                    print('could not append samecards in sameName')
                try:
                    price = recent_price(x[0])
                    duplicate_names.append([x[0], x[1], x[2], price])
                except:
                    print('could not append duplicate_names in sameName')

        except:
            print('I couldn\'t select the ids for samecards')

        try:
            print('running searchCard')
            #import pdb; pdb.set_trace()
            foil = parse_boolean(nonfoil)
            foil = not foil
            #print('does a nonfoil exist?: ',nonfoil)
            #print('foil value being sent to searchCard:', not nonfoil)
            imageUrl = searchCard(cardId, cur, priceList, foilList, dateList, imageUrl, foil)
            data = [list(x) for x in zip(dateList, priceList)]
            foildata = [list(x) for x in zip(dateList, foilList)]
        except:
            print('cant perform searchcard')
        try:
            cur.execute("select cards.cmc, type, power, toughness, rarity, cardset from cards where cards.id == ((?))",
                        (cardId, ))
            fetchInfo = cur.fetchone()
        except:
            print('could not perform id sql search')

        for value in fetchInfo:
            print('value: ', value)
        try:
            cardInfo['cmc'] = fetchInfo['cmc']
            cardInfo['type'] = fetchInfo['type']
            cardInfo['power'] = fetchInfo['power']
            cardInfo['toughness'] = fetchInfo['toughness']
            cardInfo['rarity'] = fetchInfo['rarity']
            cardInfo['buylist'] = 'N/A'
            cardInfo['cardset'] = fetchInfo['cardset']
            cardInfo['cardname'] = cardName
        except:
            print('could not add values to cardInfo dictionary')

        try:
            cur.execute('select name from cardset where code = (?)',(cardInfo['cardset'],))
            cardInfo['setname'] = cur.fetchone()[0]
            print(cardInfo['setname'])
        except:
            print('could not grab set name')

        print('the card cmc value:', cardInfo['cmc'])
        print('search value:', cardInfo['type'])
        print('power:', cardInfo['power'])

        try:
            #collecting top cards from the same set
            setcards = cur.execute('select cards.id, picurl from cards, pricetoday where cardset = ? and cards.id=pricetoday.id and cards.id != ? order by pricetoday.normprice desc limit 4', (cardInfo['cardset'],cardId))
            same_set_list = []
        except:
            print('cant sql sameset')
        try:
            for card in setcards:
                print(' same set appending list')
                print([card[0],card[1]])
                same_set_list.append([card[0],card[1]])
        except:
            print('cant find same set cards')
        try:
            cur.execute('select count(deck_meta.deckname) as count, deck_meta.deckname from deck_meta, main_deck where main_deck.cardname= ? and main_deck.uuid=deck_meta.uuid group by deck_meta.deckname order by count desc limit 3;',(cardInfo['cardname'],))
            deck_rows =cur.fetchall()
            deck_list = []
            for row in deck_rows:
                cur.execute('select deck_meta.uuid from deck_meta where upper(deck_meta.deckname) = upper(?) order by deck_meta.eventdate desc limit 1;',(row[1],))
                deck_uuid = cur.fetchone()
                #print('deck_uuid: ',deck_uuid[0])
                deck_list.append([row[0],row[1],deck_uuid[0]])

        except:
            print('could not collect decks')
            deck_list=[0]
        con.close()
    # supposed to change data input

        try:
        # 7 day SMA
            window_size = 30
            numbers = priceList
            i = 0
            moving_averages = []
            while i < len(numbers) - window_size + 1:
                this_window = numbers[i : i + window_size]

                window_average = sum(this_window) / window_size
                moving_averages.append(round(window_average,2))
                i += 1
            print(moving_averages)
            for x in range(0,window_size-1):
                moving_averages.insert(x,priceList[x])
            smadata = [list(x) for x in zip(dateList, moving_averages)]


        except:
            print('sma failed')
            smadata=0

        # chart data routed to javascript
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x', "backgroundColor":"#f5f5f5"}
        series = [{"name": 'nonfoil', "data": data},{"name":'foil', "data": foildata},{"name": 'series sma label', "data": smadata, "id":"sma","dashStyle":"Dot","color":"orange"}]
        title = {"text": ' '}
        xAxis = {"type":"datetime"}
        yAxis = {"title": {"text": ''}}
        pageType = 'graph'



        # I need to insert credits and any other variables into the html of the charts
        return render_template("resultsLayout.html",
                                pageType=pageType,
                                chartID=chartID,
                                chart=chart,
                                series=series,
                                title=title,
                                xAxis=xAxis,
                                yAxis=yAxis,
                                imageUrl=imageUrl,
                                sameCards=sameCards,
                                setCodes=setCodes,
                                cardId=cardId,
                                sameCardsCombo=duplicate_names,
                                cardInfo=cardInfo,
                                card_names=card_names,
                                price_now = price_now,
                                same_set_list=same_set_list,
                                deck_list=deck_list)

    elif request.method == "POST":
        # post means i'm adding a card to the watchlist
        print('the request was post')

        con = sql.connect(dbLoc)
        cur = con.cursor()

        valueIndicator = cardAverage.weekMonth(cardId)[2]
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)",
                        (cardId, valueIndicator, ))
            con.commit()
        except:
            print('could not insert card')
        con.close()
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows, card_names=card_names)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',card_names=card_names), 404


@app.route('/search', methods=['POST'])
def searchResults(chartID='chart_ID2', chart_type='line', chart_height=500):
    # search with the searchbar form result

    print('doing search post method')
    if request.form.get('searchbar') == None:
        print("request form searchbar is nothing:", request.form.get('addCard'))
        return "searchbar is nothing"
    else:
        #print('request form searchbar has a value')
        None

    # r is the name in string format
    try:
        fs = request.form['foil-switch']
        print('switch to foil pricing')
        print(fs)
    except:
        #print('not foil pricing')
        None

    try:
        r = (request.form['searchbar'])
        #print('r result is:', r)
    except:
        print('the r request did not go through')

    try:
        q = request.form
        #print("q:", q)
    except:
        print('cant print q')

    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()

    cardId = ""
    priceList = []
    foilList = []
    dateList = []
    imageUrl = ""
    cardInfo = {}
    sameCards = []
    duplicate_names = []
    # for the result of the name search, get the ID and put it in cardId
    try:
        for cardIdNum in cur.execute("""select ID, 
        CARDSET, PICURL from CARDS 
        where UPPER(NAME)=UPPER((?)) 
        and cards.ONLINEONLY != 'True' 
        and length(cardset)=3 
        and cardset != 'mb1'""",
                                     (r, )):
            cardId = cardIdNum[0]
            #print('cardId from execute:', cardId)
            #print('card url:',cardIdNum[2])
            # most cards have more than one printing, this compiles a list of each card
            # currently, I display the last card thats in my list I also filter to remove online cards and promos
            sameCards.append(cardIdNum[0])
            price = recent_price(cardIdNum[0])
            duplicate_names.append([cardIdNum[0], cardIdNum[1], cardIdNum[2], price])

    except:
        print('I couldnt get the cardID')

    # my test to print all the cards with the same name
    for x in sameCards:
        None
        #print('unique printing:', x)
    if not cardId:
        print('there is no card ID')
        #make a return template for fuzzy search with results
        print('fuzz ratio')
        fuzzed = process.extractBests(r,card_names,limit=10)
        print(fuzzed)
        fuzz_list = []
        for x in fuzzed:
            fuzzy_card = []
            #print(cur.execute("select id, picurl from cards where upper(name)=upper((?))",(x[0],)).fetchone()[0])
            res = cur.execute("select id, picurl from cards where upper(name)=upper((?))",(x[0],)).fetchone()
            #print('res fetchone:',res)
            for row in res:
                print('res:',row)
                fuzzy_card.append(row)
                print('appending ',row)
            fuzz_list.append(fuzzy_card)
        
        print('fuzzy_list: ',fuzz_list)
        return render_template('fuzzyReturn.html', card_names=card_names, fuzz_list=fuzz_list)
        #return render_template('frontPage.html', card_names=card_names)

    imageUrl = searchCard(cardId, cur, priceList, foilList, dateList, imageUrl,False)
    data = [list(x) for x in zip(dateList, priceList)]
    foildata = [list(x) for x in zip(dateList, foilList)]

    #print('imageUrl after searchcard:', imageUrl)
    #print('priceList to display:', priceList)

    # here I collect the bits of data I want to display, cmc, color, stats etc
    try:
        print('selecting data to display')
        cur.execute("""select 
        cmc, 
        type, 
        power, 
        toughness, 
        rarity,
        cardset,
        name
        from cards 
        where id == ((?))""",
                    (cardId, ))
        fetchInfo = cur.fetchone()
        print('cardID: ', cardId)
        print('fetch one for sql:')
        for x in fetchInfo:
            print(x)
        price_now = recent_price(cardId)

        for value in fetchInfo:
            print('value: ', value)
    except:
        print('could not select sql returns for cardInfo')
    try:
        cardInfo['cmc'] = fetchInfo[0]
        cardInfo['type'] = fetchInfo[1]
        cardInfo['power'] = fetchInfo[2]
        cardInfo['toughness'] = fetchInfo[3]
        cardInfo['rarity'] = fetchInfo[4]
        cardInfo['buylist'] = 'N/A'
        cardInfo['cardset'] = fetchInfo[5]
        cardInfo['cardname'] = fetchInfo[6]
        print('card set: ',cardInfo['cardset'])
    except:
        print('could not add values to cardInfo dictionary here')
    try:
        cur.execute('select name from cardset where code = (?)',(cardInfo['cardset'],))
        cardInfo['setname'] = cur.fetchone()[0]
        print('card set name: ',cardInfo['setname'])
        print('set name:',cardInfo['setname'])
    except:
        print('could not grab set name')

    print('the card cmc value:', cardInfo['cmc'])
    print('search value:', cardInfo['type'])
    print('power:', cardInfo['power'])

    con.close()

    try:
        # 7 day SMA
        window_size = 30
        numbers = priceList
        i = 0
        moving_averages = []
        while i < len(numbers) - window_size + 1:
            this_window = numbers[i : i + window_size]

            window_average = sum(this_window) / window_size
            moving_averages.append(round(window_average,2))
            i += 1
        print(moving_averages)
        for x in range(0,window_size-1):
            moving_averages.insert(x,priceList[x])
        smadata = [list(x) for x in zip(dateList, moving_averages)]


    except:
        print('sma failed')

    # chart data
    try:
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x', "backgroundColor":"#f5f5f5"}
        series = [{"name": 'nonfoil', "data": data},{"name":'foil', "data": foildata},{"name": 'series sma label', "data": smadata, "id":"sma","dashStyle":"Dot","color":"orange"}]
        title = {"text": ''}
        xAxis = {"type":"datetime"}
        yAxis = {"title": {"text": 'dollars'}}
        pageType = 'graph'


    except:
        print('something went wrong with the highcart vars')

    return render_template("resultsLayout.html",
                           pageType=pageType,
                           chartID=chartID,
                           chart=chart,
                           series=series,
                           title=title,
                           xAxis=xAxis,
                           yAxis=yAxis,
                           imageUrl=imageUrl,
                           sameCards=sameCards,
                           cardId=cardId,
                           sameCardsCombo=duplicate_names,
                           cardInfo=cardInfo,
                           card_names=card_names,
                           price_now = price_now)

def searchCard(cardId, cur, priceList, foilList, dateList, imageUrl, foil):
    # for the url I make the variable the string, and for the date and price I add them to the lists
    #import pdb; pdb.set_trace()
    try:
        print('im doing a search card for:', cardId)
        print('card foil value:',foil)
    except:
        print('could not start searchCard')
    try:
        for cardUrl in cur.execute("select PICURL from cards where id=(?)", (cardId,)):
            imageUrl = cardUrl[0]
            print('imageURL from searchcard:', imageUrl)
            # if the card is only foil, get foil prices. else get nonfoil prices
    except:
        print('could not collect cardurl in searchCard')

    try:
        print('card in searchCard is nonfoil')
        for priceN in cur.execute("select datetime,normprice,foilprice from prices where id=(?) order by datetime asc", (cardId,)):
            if priceN[1] is None:
                priceList.append(0)
            else:
                priceList.append(priceN[1])
    
            if priceN[2] is None:
                foilList.append(0)
            else:
                foilList.append(priceN[2])
            # the date is stored with dash marks but needs to be displayed with slashes
            # also js needs the timestamps multiplied by 1000 for unix time or some shit
            # this block of text made it hell to display charts across different parts of the site because of the date format changes
            newdate = priceN[0].replace("-","/")
            time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
            timestamp = datetime.datetime.timestamp(time_element)
            timestamp = int(timestamp)
            timestamp = timestamp*1000
            dateList.append(timestamp)
    except:
        print('could not detect foil status in cardSearch')


        """
        for x in dateList:
            print('datelist val:')
            print(datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        """
    return imageUrl
    print('dateList:')


def updateTrend(cardId):
    print('running updateTrend for', cardId)
    try:
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        print('connected to db')
    except:
        print('couldnt connect to db')

    try:
        valueIndicator = ""
        valueIndicator = cardAverage.weekMonth(cardId)[2]
        print('collected cardAverage')
    except:
        print('could not perform cardAverage')
    # insert to watchlist
    try:
        cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)",
                    (cardId, valueIndicator, ))
        con.commit()
        con.close()
    except:
        print('could not update card with updateTrend')
        con.close()


@app.route('/search', methods=['GET'])
def searchGet():
    return render_template("searchGetLayout.html", card_names=card_names)


@app.route('/pandas')
def topCards():

    # tensorflow/keras processing could go here in the future

    # return render_template("topLayout.html", rows = rows)
    return render_template("topLayout.html", card_names=card_names)


@app.route('/collection', methods=['GET', 'POST'])
def collectionPage():
    collection_rows = getCollection()
    today = getTime()

    try:
        # grab the chart values for today: total mrsp, and what I paid
        # push those numbers to the database for today's date
        cardsDb = sql.connect(dbLoc)
        cursor = cardsDb.cursor()
        todays_price, total_msrp, total_paid = collection_tally(
            collection_rows, cursor, today)
        tally_pusher(round(total_msrp,2), round(total_paid,2), cursor, today)
        cardsDb.commit()
        cardsDb.close()
        print('ran collection tally and pusher')
    except:
        print('could not run collection tally or pusher')
        print('values:')
        no_val = [todays_price, total_msrp, total_paid]
        for x in no_val:
            try:
                print(x)
            except:
                print('could not print val')

    if request.method == "GET":
        None
    # if its a post and adding a card from the form
    elif request.method == "POST" and request.form.get('removeCard') == None:

        try:
            # html form request
            user_id = 'timtim'
            cost_paid = 3
            number_owned = 1
            card_name = (request.form['name-form'])
            set_code = (request.form['set-form'])
            cost_paid = (request.form['cost-form'])
            number_owned = (request.form['number-form'])
        except:
            print('could not request html form data')

        try:
            # check form data results for missing info
            if number_owned is '':
                print('number owned is none')
                number_owned = 1
            else:
                print('number owned is not none')

            if cost_paid is '':
                print('cost is none')
                cost_paid = 0
            else:
                print('cost is not none')

            if set_code is '':
                print('set code is none')
                cardsDb = sql.connect(dbLoc)
                cursor = cardsDb.cursor()
                cursor.execute('''select cardset,
                id 
                from cards 
                where upper(name)=upper(?) 
                and cards.ONLINEONLY != "True" 
                and length(cardset)=3
                and nonfoil = "True"
                ''',
                               (card_name,))
                set_code, card_id = cursor.fetchone()
                cardsDb.close()
            else:
                print('set code is known')
        except:
            print('something went wrong checking form data results')

        try:
            # select id from cards
            cardsDb = sql.connect(dbLoc)
            cursor = cardsDb.cursor()
            card_id = cursor.execute('''select id 
            from cards 
            where upper(name) = upper((?)) 
            and upper(cardset) = upper((?))''',
                                     (card_name, set_code,))
            cardid = card_id.fetchone()[0]
            print('cardid:', cardid)
        except:
            print('could not select id from cards')

        try:
            print('selecting latest normprice')
            cursor.execute('''select normprice 
            from prices where id = (?) 
            order by datetime desc''',
                           (cardid,))
            price = cursor.fetchone()
            print('card normprice:', price[0])
            if price[0] == None:
                print('price[0] is None')
                price[0] = 0
        except:
            print('could not select latest normprice')
        try:
            # insert into collections
            cursor.execute('''insert into collections 
            (user_id, 
            card_id, 
            cost_paid, 
            msrp, 
            number_owned, 
            name, 
            code, 
            datetime, 
            transaction_id) 
            values (?, ?, ?, ?, ?, ?, ?, ?, NULL)''',
                           (user_id,
                            cardid,
                            cost_paid,
                            price[0],
                            number_owned,
                            card_name,
                            set_code,
                            today, ))
            cardsDb.commit()
        except:
            print('could not insert into collections')
            unable = [user_id,
                      cardid,
                      cost_paid,
                      price[0],
                      number_owned,
                      card_name,
                      set_code,
                      today]
            for x in unable:
                try:
                    print(x)
                except:
                    print('cant print this val')

        try:
            # print collections, run getCollection
            for x in cursor.execute('select * from collections'):
                print(x)
            collection_rows = getCollection()
        except:
            print('could not run getCollection')

        try:
            # pusher
            todays_price, total_msrp, total_paid = collection_tally(
                collection_rows, cursor, today)
            #round the value of total_msrp
            total_msrp = round(total_msrp, 2)
            # pushes new information so graph will have current info
            tally_pusher(total_msrp, total_paid, cursor, today)
            cardsDb.commit()
            cardsDb.close()
        except:
            print('couldnt run collection tally, or pusher')
            print('values:')
            mis_val = []

    else:
        print("remove card post collection")
        con = sql.connect(dbLoc)
        cur = con.cursor()
        transaction_id = request.form.get('removeCard')

        try:
            cur.execute(
                "delete from collections where transaction_id=(?)", (transaction_id, ))
            print('removed ', transaction_id, ' from collections')
        except:
            print('could not remove card from collections')
        con.commit()
        con.close()

        collection_rows = getCollection()

        cardsDb = sql.connect(dbLoc)
        cursor = cardsDb.cursor()
        todays_price, total_msrp, total_paid = collection_tally(
            collection_rows, cursor, today)
        # pushes new information so graph will have current info
        tally_pusher(total_msrp, total_paid, cursor, today)
        cardsDb.commit()
        cardsDb.close()

    p = price_chart()
    try:
        perc = int(total_msrp/total_paid * 100)
    except:
        perc = 0

    return render_template("collection.html",
                           collection_rows=collection_rows,
                           todays_price=todays_price,
                           perc=perc,
                           total_msrp=round(total_msrp, 2),
                           total_paid=round(total_paid, 2),
                           pageType=p[5],
                           chartID="chart_ID",
                           chart=p[0],
                           series=p[1],
                           title=p[2],
                           xAxis=p[3],
                           yAxis=p[4],
                           card_names=card_names)


# functions
def getWatchList():
    # this is a function to get the watchlist results which I use in my GET and POST for /watchlist
    print('running getwatchlist')
    try:
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        print('connected to db')
    except:
        print('could not connect to db')
    try:
        cur.execute("""select cards.name, 
        watchlist.pricedirection, 
        cards.id 
        from watchlist, 
        cards 
        where watchlist.id = cards.id""")
        rows = cur.fetchall()
    except:
        print('could not select watchlist')

    for x in rows:
        print(x['id'])

    con.close()
    return rows


def getCollection():
    # selects existing card information from collection db
    print('running getCollection')
    try:
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        print('connected to db')
    except:
        print('could not connect to db')
    try:
        cur.execute("select * from collections where user_id = 'timtim'")
    except:
        print('could not select collection')
    try:
        rows = cur.fetchall()
        print('selecting all collection values for timtim:')
    except:
        print('could not fetch all collection')

    try:
        for x in rows:
            print(x['name'])
    except:
        print('could not print rows')
    con.close()
    try:
        print('returning rows')
        return rows
    except:
        print('get_collection returned nothing')
        return []


def getTime():
    # returns todays date in string format
    ts = time.time()
    dailyTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    print('test getTime:', dailyTime)
    return dailyTime


def yesterday():
    # returns yesterdays date in string format
    ts = time.time() - 86400
    dailyTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    print('test yesterday:', dailyTime)
    return dailyTime


def collection_tally(collection_rows, cursor, today):
    # counts up values of the cards listed in user's collection
    # returns the total values
    print('running collection tally')
    todays_price = []
    total_msrp = 0
    total_paid = 0

    for card in collection_rows:
        cursor.execute('''select normprice 
                        from prices 
                        where id = (?) 
                        order by datetime desc''', (card["card_id"],))
        try:
            prix = cursor.fetchone()
            try:
                if prix[0] == None:
                    print('prix is None')
                    prix[0] = 0
                else:
                    print('price is:', prix[0])
            except:
                print('could not fix prix')
            print('prix is:', [prix])
            todays_price.append(prix)
            print('number owned:', card["number_owned"])
            total_msrp = total_msrp + card["number_owned"] * prix[0]
            total_paid = total_paid + card["number_owned"] * card["cost_paid"]
        except:
            print('something went wrong with collection_tally calculations')

        # total_paid could also go here
    return todays_price, total_msrp, total_paid


def tally_pusher(total_msrp, total_paid, cursor, today):
    # push the daily tally to a db
    # this is a wrapper for a user's tally. I currently have it hardcoded to "timtim".
    print('running tally pusher:')
    print('todays msrp is:', total_msrp)
    try:
        cursor.execute('''insert or replace 
        into COLLECTION_VAL 
        (USER_ID,COL_VAL,PAID_VAL,DATETIME) 
        values (?,?,?,?)''',
                       ("timtim", total_msrp, total_paid, today,))
        print('tally pushed')
    except:
        print('could not push tally')
    print('tally pusher ending')


def price_chart():
    # used for displaying collection highcart
    # returns values in a dictionary
    print('running price_chart')
    try:
        print('refreshing chart data')
        cardsDb = sql.connect(dbLoc)
        cursor = cardsDb.cursor()
        chart_vals = cursor.execute("""select DATETIME,
        COL_VAL, 
        PAID_VAL 
        from collection_val 
        order by datetime asc""")
    except:
        print('could not refresh chart data')
    x_ax = []
    y_ax = []
    z_ax = []
    try:
        for vals in chart_vals:
            print(vals)
            # the date needs a reformat to display on highcharts
            # this may appear to be confusing, because it is.
            # javascript needs unix time multiplied by 1000, and I store
            # dates with hyphens instead of slashes.
            newdate = vals[0].replace("-","/")
            time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
            timestamp = datetime.datetime.timestamp(time_element)
            timestamp = int(timestamp)
            timestamp = timestamp*1000
            #print(timestamp)
            x_ax.append(timestamp)
            #x_ax.append(vals[0])

            y_ax.append(vals[1])
            z_ax.append(vals[2])
        cardsDb.close()
    except:
        print('could not append chart_vals')
        cardsDb.close()

    #convert values to data list
    dateList = x_ax
    priceList1 = y_ax
    priceList2 = z_ax
    data = [list(x) for x in zip(dateList, priceList1, priceList2)]
    print('data:')
    print(data)


    # chart insertion




    try:
        chart = {"renderTo": "chart_ID", "type": "area",
                 "height": 500, "zoomType": 'x', "backgroundColor":"#f5f5f5"}
        series = [{"name": 'series label', "data": data}]
        title = {"text": "cost vs value"}
        xAxis = {'type': 'datetime'}
        yAxis = {"title": {"text": 'Price in dollars'}}
        pageType = 'graph'
    except:
        print('something went wrong with the highcart vars')
    # this line converts lists of my dates to date objects.
    # change "datetime" at the end to the list's name(x_ax in this case)
    # dates_list = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in datetime]
    return [chart, series, title, xAxis, yAxis, pageType]


def buy_vs_tcg():
    None
    '''select buylist.DATETIME,
     buylist.BUYPRICE,
      prices.NORMPRICE from 
      buylist,
      cardset,
      cards,
      prices 
      where upper(cardset.NAME) = upper(buylist.SETNAME) 
      and buylist.name = "Land Tax" 
      and buylist.SETNAME = "battlebond" 
      and cardset.code = cards.CARDSET 
      and cards.NAME = buylist.NAME 
      and prices.id = cards.ID 
      and buylist.datetime=prices.DATETIME 
      order by buylist.datetime'''


def get_id(name, setCode):
    # returns card ID with a name and set code
    con = sql.connect(dbLoc)
    cursor = con.cursor()
    cursor.execute('''select cards.id 
    from cards 
    where upper(cards.name) = upper(?) 
    and cards.cardset = (?)''',
                   (name, setCode))
    card_id = cursor.fetchone()
    print('card_id:', card_id)
    con.close()
    return card_id

def recent_price(cardID):
    if cardID is None:
        return 0
    #print('starting recent_price for ',cardID)
    con = sql.connect(dbLoc)
    cursor = con.cursor()
    cursor.execute('''select normprice, foilprice from prices where ID = (?) 
    order by datetime desc''',
                   (cardID, ))
    price = cursor.fetchone()
    normalprice = price[0]
    foilprice = price[1]
    con.close()
    if normalprice is None:
        print('normalprice is none checking for foil')
        if foilprice is None:
            price = 0
        else:
            price = foilprice
    else:
        price = normalprice
    #print('price:',price)
    #print('finished recent_price search')
    return price

def parse_boolean(b):
    return b == "True"

if __name__ == "__main__":
    app.run(debug=True)

