from flask import Flask, render_template, request
import sqlite3 as sql
import cardAverage
import datetime
import time


# This is my flask file which runs the application

app = Flask(__name__)

# the location of the database, when running locally vs on server
#dbLoc = '/home/timc/flask_project/flask_app/CARDINFO.db'

#website location
#dbLoc = 'CARDINFO.db'

#windows local
dbLoc = 'C:/Users/Tim/Documents/pythonScripts/mimicvat/CARDINFO.db'


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
    dateList = []
    cardId = "810a3792-a689-4849-bc14-fb3c71153aba"
    imageUrl = ""
    cardName = "Land Tax"

    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()

    imageUrl = 'https://img.scryfall.com/cards/normal/front/8/1/810a3792-a689-4849-bc14-fb3c71153aba.jpg?1562920975'

# @app.route('/movers', methods=['GET', 'POST'])
# def method_name():
#    pass

# collects price and date vals of land tax to load up front page quickly
    land_tax_vals = cur.execute(
        "select * from frontpage order by datetime asc")

    for vals in land_tax_vals:
        priceList.append(vals[1])
        dateList.append(vals[0])
    con.close()

    # chart insertion
    try:
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList, "id":"dataset"},
        {"type":"roc", "linkedTo":"dataset","params":{"period":"10"}}]
        title = {"text": cardName}
        xAxis = [{"categories": dateList}, {'type': 'datetime'}]
        yAxis = {"title": {"text": 'Price in dollars'}}
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

@app.route('/sets')
def setsPage():
    try:
        con = sql.connect(dbLoc)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select name, code from cardset where substr(name,-6,6) != 'Tokens' and substr(name,-6,6) != 'Promos' and substr(name,-9,9) != 'Oversized'")
        rows = cur.fetchall()
        con.close()
        setnames = rows
    except:
        print('could not collect set data')
        setnames = []
    return render_template("sets.html", setnames = setnames,card_names=card_names)

@app.route('/setinfo/<setid>', methods=['GET', 'POST'])
def setinfo(setid):
    try:
        print('connecting to db')
        con = sql.connect(dbLoc)
        #con.row_factory = sql.Row
        cur = con.cursor()
    except:
        print('could not connect to db in setinfo')
    try:
        print(setid)
        print(type(setid))
    except:
        print('could not print setid or type')
    try:

        setcards = cur.execute('select id, name, picurl from cards where cardset = ?', (setid,))
        return_list = []
        for card in setcards:
            return_list.append(list(card))
        for card in return_list:
            price_val = cur.execute('select normprice from prices where id=? and datetime = ?',(card[0],'2019-07-24'))
            print(card[0],' price: ',cur.fetchone())
        print(return_list)

        """
        for card in setcards:
            print('searching for price:',card[0],'name:',card[1])
        """
            #normp, foilp = cur.execute('select normprice, foilprice from prices where id = ?', (card[0],))
        #setcards = cur.execute('select cards.id, cards.name, normprice, foilprice, picurl from cards, prices where prices.id = cards.id and cardset = ? and prices.datetime = ?', (setid,'2019-07-24',))
        #select datetime,normprice from prices where id=(?) order by datetime asc
        #date field needs to be getTime() in production environment
        setnorm = 0
        setfoil = 0
        ratio = 0
        print('fetch one:',cur.fetchone()[0])
    except:
        print('could not collect id name and picurl')
    """
    try:
        print('performing normal vs foil calc')
        for row in setcards:
            print('name:',row[0])
            setnorm = setnorm + row[2]
            setnorm = round(setnorm,2)
            setfoil = setfoil + row[3]
            setfoil = round(setfoil,2)
            ratio = setfoil/setnorm
            ratio = round(ratio,2)
    except:
        print('could not perform norm vs foil calc')


    try:
        if cur.fetchone() is None:
            ratio = 0
    except:
        print('could not fetchone')
    """

    #return render_template('setinfo.html',setnorm = setnorm,setfoil=setfoil,ratio=ratio,setcode=setid,carddeck = setcards)
    return render_template('setinfo.html',setcode=setid, carddeck = return_list,card_names=card_names)


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
        reserved_vals = cur.execute(
            "select * from reservedhistory order by datetime asc")
    except:
        print('could not select')

    try:
        print('appending chart lists')
        for vals in reserved_vals:
            print('vals:',vals[1],vals[0])
            priceList.append(vals[1])
            dateList.append(vals[0].replace("-","/"))
    except:
        print('could not append chart lists')
    con.close()

    # chart insertion
    try:
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": 'reserved list'}
        xAxis = [{"categories": dateList}, {'type': 'datetime'}]
        yAxis = {"title": {"text": 'Price in dollars'}}
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
                        card_names=card_names)

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
        dateList = []
        imageUrl = ""
        sameCards = []
        setCodes = []
        duplicate_names = []
        cardInfo = {}
        cardName = ""

        # selects name and set of the card
        try:
            for x in cur.execute("select NAME, CARDSET from CARDS where ID=(?)", (cardId, )):
                print('the name is:', x[0])
                print('the set is:', x[1])
                cardName = x[0]
                setCodes.append(x[1])
        except:
            print('I couldnt get the card name')

        # select ids of all reprints
        print('card im looking up:', cardId)
        try:
            for x in cur.execute("""select id, 
            cardset 
            from cards 
            where name = (?) 
            and cards.ONLINEONLY != 'True'""", (cardName,)):
                try:
                    sameCards.append(x[0])
                except:
                    print('could not append samecards in sameName')
                try:
                    duplicate_names.append([x[0], x[1]])
                except:
                    print('could not append duplicate_names in sameName')

                print("i found an ID")
                print("x 0:", x[0])
                print("x 1:", x[1])
            print('duplicate_names:', duplicate_names)
        except:
            print('I couldn\'t select the ids for samecards')

        try:
            print('running searchCard')
            imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)
            print('prices:', priceList)
        except:
            print('cant perform searchcard')
        try:
            cur.execute("select cards.cmc, type, power, toughness, rarity from cards where cards.id == ((?))",
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
        except:
            print('could not add values to cardInfo dictionary')

        print('the card cmc value:', cardInfo['cmc'])
        print('search value:', cardInfo['type'])
        print('power:', cardInfo['power'])

        con.close()

        # chart data routed to javascript
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": cardName}
        xAxis = {"categories": dateList, "type":'datetime'}
        yAxis = {"title": {"text": 'Dollars'}}
        pageType = 'graph'
        # I need to insert credits and any other variables into the html of the charts
        return render_template("resultsLayout.html",
                               pageType=pageType,
                               chartID=chartID,
                               chart=chart,
                               series=series,
                               #title=title,
                               xAxis=xAxis,
                               yAxis=yAxis,
                               imageUrl=imageUrl,
                               sameCards=sameCards,
                               setCodes=setCodes,
                               cardId=cardId,
                               sameCardsCombo=duplicate_names,
                               cardInfo=cardInfo,
                               card_names=card_names)

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
        print('request form searchbar has a value')

    # r is the name in string format
    try:
        r = (request.form['searchbar'])
        print('r result is:', r)
    except:
        print('the r request did not go through')

    try:
        q = request.form
        print("q:", q)
    except:
        print('cant print q')

    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()

    cardId = ""
    priceList = []
    dateList = []
    imageUrl = ""
    cardInfo = {}
    sameCards = []
    duplicate_names = []
    # for the result of the name search, get the ID and put it in cardId
    try:
        print('checking for every card with the name:', r)
        searchResult = cur.execute("""select id, 
        cardset 
        from cards 
        where name = (upper(?)) 
        and cards.ONLINEONLY != 'True' 
        and length(cardset)=3""", (r,))

        print('looking at:', searchResult)

        if not searchResult:
            print('there was no search result')
            return 'there was no search result'
        for x in searchResult:
            print('value of x:', x)
            if not x:
                print('there was no search result')
                return "there was no search result"
            try:
                sameCards.append(x[0])
                print('appending samecards with :', x[0])
            except:
                print('could not append samecards in sameName')
            try:
                duplicate_names.append([x[0], x[1]])
            except:
                print('could not append duplicate_names in sameName')

            print("x 0:", x[0])
            print("x 1:", x[1])
        print('duplicate_names:', duplicate_names)

    except:
        print('I couldnt select the ids for samecards')

    try:
        for cardIdNum in cur.execute("""select ID, 
        CARDSET from CARDS 
        where UPPER(NAME)=UPPER((?)) 
        and cards.ONLINEONLY != 'True' 
        and length(cardset)=3 
        and cardset != 'mb1'""",
                                     (r, )):
            cardId = cardIdNum[0]
            print('cardId from execute:', cardId)
            # most cards have more than one printing, this compiles a list of each card
            # currently, I display the last card thats in my list I also filter to remove online cards and promos
            sameCards.append(cardIdNum[0])
            duplicate_names.append([cardIdNum[0], cardIdNum[1]])
    except:
        print('I couldnt get the cardID')

    # my test to print all the cards with the same name
    for x in sameCards:
        print('unique printing:', x)
    if not cardId:
        print('there is no card ID')
        return render_template('frontPage.html', card_names=card_names)
    imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)

    print('imageUrl after searchcard:', imageUrl)
    print('priceList to display:', priceList)

    # here I collect the bits of data I want to display, cmc, color, stats etc
    cur.execute("""select 
    cmc, 
    type, 
    power, 
    toughness, 
    rarity 
    from cards 
    where id == ((?))""",
                (cardId, ))
    fetchInfo = cur.fetchone()

    for value in fetchInfo:
        print('value: ', value)
    try:
        cardInfo['cmc'] = fetchInfo[0]
        cardInfo['type'] = fetchInfo[1]
        cardInfo['power'] = fetchInfo[2]
        cardInfo['toughness'] = fetchInfo[3]
        cardInfo['rarity'] = fetchInfo[4]
        cardInfo['buylist'] = 'N/A'
    except:
        print('could not add values to cardInfo dictionary here')

# cur.execute("""select buylist.BUYPRICE,
# buylist.DATETIME
# from buylist,
# cards,
# CARDSET
# where cards.id == ((?))
# and cards.CARDSET = CARDSET.CODE
# and upper(cardset.name) = upper(replace (buylist.SETNAME,'-',' '))
# and upper(cards.name) = upper(buylist.NAME)
# order by datetime desc""",
# (cardId, ))

    print('the card cmc value:', cardInfo['cmc'])
    print('search value:', cardInfo['type'])
    print('power:', cardInfo['power'])

    con.close()

    # chart data
    try:
        chart = {"renderTo": chartID, "type": chart_type,
                 "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": r}
        xAxis = [{"categories": dateList, "type":"datetime"}]
        yAxis = {"title": {"text": 'Price in dollars'}}
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
                           card_names=card_names)


def searchCard(cardId, cur, priceList, dateList, imageUrl):
    # for the url I make the variable the string, and for the date and price I add them to the lists
    #import pdb; pdb.set_trace()
    print('im doing a search card for:', cardId)
    try:
        for cardUrl in cur.execute("select PICURL from cards where id=(?)", (cardId,)):
            imageUrl = cardUrl[0]
            print('imageURL from searchcard:', imageUrl)
            # if the card is only foil, get foil prices. else get nonfoil prices

            # this for loop is what makes loading a search slow
        for priceN in cur.execute("select datetime,normprice from prices where id=(?) order by datetime asc", (cardId,)):
            if priceN[1] is None:
                priceList.append(0)
            else:
                priceList.append(priceN[1])
            newdate = priceN[0].replace("-","/")
            time_element= datetime.datetime.strptime(newdate,"%Y/%m/%d")
            timestamp = datetime.datetime.timestamp(time_element)
            timestamp = int(timestamp)
            timestamp = timestamp*1000
            #print(timestamp)
            dateList.append(timestamp)
            #dateList.append(priceN[0].replace("-","/"))
        #print('dateList:')
        #print(dateList)
        """
        for x in dateList:
            print('datelist val:')
            print(datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
        """
        return imageUrl
    except:
        print('the for-loops didnt work for cardUrl and price chart lists')
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
            x_ax.append(vals[0])
            y_ax.append(vals[1])
            z_ax.append(vals[2])
        cardsDb.close()
    except:
        print('could not append chart_vals')
        cardsDb.close()

    # chart insertion

    try:
        chart = {"renderTo": "chart_ID", "type": "area",
                 "height": 500, "zoomType": 'x'}
        series = [{"name": "MSRP", "data": y_ax},
                  {"name": "Paid", "data": z_ax}]
        title = {"text": "cost vs value"}
        xAxis = [{"categories": x_ax}, {'type': 'datetime'}]
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


if __name__ == "__main__":
    app.run(debug=True)
