from flask import Flask, render_template, request
import sqlite3 as sql
import cardAverage


# This is my flask file which runs the application

app = Flask(__name__)

# the location of the database, when running locally vs on server
#dbLoc = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbLoc = 'CARDINFO.db'


#
# App routes:
#
# index: the front page, I have a static card example to show the site's features
# list: I fetch and display a set of cards so users can see what kind of data I have
# watchlist: a list of cards users can modify to track cards with
# search: a series of get/post routes for searching for specific cards
# topcards: an experimental page for displaying useful statistics and potential future features.
# i'm currently working on integrating machine learning with keras to this section, and also a
# card generator page with an lstm model just for fun
#


@app.route('/')
def index(chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):
    # the front page with bootstrap layout parent, and static example card
    priceList = []
    dateList = []
    cardId = "810a3792-a689-4849-bc14-fb3c71153aba"
    imageUrl = ""
    cardName = "Land Tax"


    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)

    # chart insertion
    try:
        subtitleText = 'the price chart'
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": cardName}
        xAxis = {"categories": dateList}
        yAxis = {"title": {"text": 'Price in dollars'}}
        pageType = 'graph'
    except:
        print('something went wrong with the highcart vars')

    con.close()
    return render_template('frontPage.html', pageType=pageType, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, imageUrl=imageUrl, cardId = cardId, cardName = cardName)

@app.route('/list')
def listPage():
    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from CARDS where cardset='aer'")
    rows = cur.fetchall()
    con.close()

    return render_template("listLayout.html", rows = rows)

@app.route('/watchlist', methods=['POST', 'GET'])
def watchlist():

    if request.method == 'GET':
        print('watchlist get request')
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows = rows)

    elif request.form.get('removeCard') == None:
        print('/watchlist post request insert')
        con = sql.connect("CARDINFO.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        r = (request.form['watchlist'])

        cardId = ""
        valueIndicator = ""

        # card ID fetching
        try:
            for cardIdNum in cur.execute("select ID from CARDS where UPPER(NAME)=UPPER((?))", (r, )):
                cardId = cardIdNum[0]
        except:
            print('could not find card')

        # the cardAverage week/month for the searched card
        valueIndicator = cardAverage.weekMonth(cardId)[2]

        # insert to watchlist
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)", (cardId, valueIndicator, ) )
            con.commit()
            con.close()
        except:
            print('could not insert card')

        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows)

    # post request to remove card from list
    else:
        print("remove card post request")
        con = sql.connect("CARDINFO.db")
        cur = con.cursor()
        cardID = request.form.get('removeCard')

        try:
            cur.execute("delete from watchlist where ID=(?)", (cardID, ))
            print('removed ',cardID,' from watchlist')
        except:
            print('could not remove card from watchlist')
        con.commit()
        con.close()

        rows = getWatchList()

        return render_template("watchlistLayout.html", rows = rows)

@app.route('/search/<cardId>', methods=['GET', 'POST'])
def searchID(cardId, chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):
    # the search bar results for the layout html
    if request.method == "GET":
        print('search cardID get request')
        con = sql.connect("CARDINFO.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        # initializing my variables, cardId as a string, pricelist/datelist for graph, imageurl as string
        priceList = []
        dateList = []
        imageUrl = ""
        sameCards = []
        setCodes = []
        sameCardsCombo = []
        cardInfo = {}
        cardName = ""

        # selects name and set of current card
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
            for x in cur.execute("select id, cardset from cards where name = (select name from cards where id = \"" + cardId + "\") and cards.ONLINEONLY != 'TRUE'"):
                try:
                    sameCards.append(x[0])
                except:
                    print('could not append samecards in sameName')
                try:
                    sameCardsCombo.append([x[0], x[1]])
                except:
                    print('could not append sameCardCombo in sameName')
                    
                print("i found an ID")
                print("x 0:",x[0])
                print("x 1:",x[1])
            print('samecardcombo:',sameCardsCombo)
        except:
            print('I couldnt select the ids for samecards')

        try:
            imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)
        except:
            print('cant perform searchcard')

        cur.execute("select cards.cmc, type, power, toughness, rarity from cards where cards.id == ((?))",(cardId, ))
        fetchInfo = cur.fetchone()

        for value in fetchInfo:
            print('value: ',value)
        try:
            cardInfo['cmc'] = fetchInfo[0]
            cardInfo['type'] = fetchInfo[1]
            cardInfo['power'] = fetchInfo[2]
            cardInfo['toughness'] = fetchInfo[3]
            cardInfo['rarity'] = fetchInfo[4]
        except:
            print('could not add values to cardInfo dictionary')

        try:
            cur.execute("select buylist.BUYPRICE, buylist.DATETIME from buylist, cards, CARDSET where cards.id == ((?))  and cards.CARDSET = CARDSET.CODE  and upper(cardset.name) = upper(replace (buylist.SETNAME,'-',' ')) and upper(cards.name) = upper(buylist.NAME) order by datetime desc",(cardId, ))
        except:
            print('could not select buylist price, probably no buylist value')

        try:
            fetchInfo = cur.fetchone()
            cardInfo['buylist'] = fetchInfo[0]
        except:
            print('could not add buylist to dictionary, probaby no buylist value')

        print('the card cmc value:', cardInfo['cmc'])
        print('search value:', cardInfo['type'])
        print('power:',cardInfo['power'])

        con.close()

        # chart data routed to javascript
        subtitleText = 'the price chart'
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": cardName}
        xAxis = {"categories": dateList}
        yAxis = {"title": {"text": 'Price in dollars'}}
        pageType = 'graph'

        return render_template("resultsLayout.html", pageType=pageType, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, imageUrl=imageUrl, sameCards = sameCards, setCodes = setCodes, cardId = cardId, sameCardsCombo = sameCardsCombo, cardInfo = cardInfo)

    elif request.method == "POST":
        # post means i'm adding a card to the watchlist
        print('the request was post')

        con = sql.connect("CARDINFO.db")
        cur = con.cursor()

        valueIndicator = cardAverage.weekMonth(cardId)[2]
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)", (cardId, valueIndicator, ) )
            con.commit()
        except:
            print('could not insert card')
        con.close()
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows = rows)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/search', methods=['POST'])
def searchResults(chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):
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

    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cardId = ""
    priceList = []
    dateList = []
    imageUrl = ""
    cardInfo = {}
    sameCards = []
    sameCardsCombo = []
    # for the result of the name search, get the ID and put it in cardId
    try:
        print('checking for more cards with the same name as ',r)
        searchResult = cur.execute("select id, cardset from cards where name = (select name from cards where upper(name) = \"" + r.upper() + "\") and cards.ONLINEONLY != 'TRUE'")
        print('looking at:',searchResult)
        if not searchResult:
            print('there was no search result')
            return 'there was no search result'
        for x in searchResult:
            print('value of x:',x)
            if not x:
                print('there was no search result')
                return "there was no search result"
            try:
                sameCards.append(x[0])
                print('appending samecards with :',x[0])
            except:
                print('could not append samecards in sameName')
            try:
                sameCardsCombo.append([x[0], x[1]])
            except:
                print('could not append sameCardCombo in sameName')

            print("x 0:",x[0])
            print("x 1:",x[1])
        print('samecardcombo:',sameCardsCombo)

    except:
        print('I couldnt select the ids for samecards')

    try:
        for cardIdNum in cur.execute("select ID, CARDSET from CARDS where UPPER(NAME)=UPPER((?))", (r, )):
            cardId = cardIdNum[0]

            # most cards have more than one printing, this compiles a list of each card
            # currently, I display the last card thats in my list
            sameCards.append(cardIdNum[0])
    except:
        print('I couldnt get the cardID')

    # my test to print all the cards with the same name
    for x in sameCards:
        print(x)
    if not cardId:
        print('there is no card ID')
        return render_template('frontPage.html')
    imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)
    print('imageUrl after searchcard:', imageUrl)

    # here I collect the bits of data I want to display, cmc, color, stats etc
    cur.execute("select cards.cmc, type, power, toughness, rarity from cards where cards.id == ((?))",(cardId, ))
    fetchInfo = cur.fetchone()

    for value in fetchInfo:
        print('value: ',value)
    try:
        cardInfo['cmc'] = fetchInfo[0]
        cardInfo['type'] = fetchInfo[1]
        cardInfo['power'] = fetchInfo[2]
        cardInfo['toughness'] = fetchInfo[3]
        cardInfo['rarity'] = fetchInfo[4]
    except:
        print('could not add values to cardInfo dictionary here')

    try:
        cur.execute("select buylist.BUYPRICE, buylist.DATETIME from buylist, cards, CARDSET where cards.id == ((?))  and cards.CARDSET = CARDSET.CODE  and upper(cardset.name) = upper(replace (buylist.SETNAME,'-',' ')) and upper(cards.name) = upper(buylist.NAME) order by datetime desc",(cardId, ))
    except:
        print('could not select buylist price, probably no buylist value')

    try:
        fetchInfo = cur.fetchone()
        cardInfo['buylist'] = fetchInfo[0]
    except:
        print('could not add buylist to dictionary, probaby no buylist value')


    print('the card cmc value:', cardInfo['cmc'])
    print('search value:', cardInfo['type'])
    print('power:',cardInfo['power'])

    con.close()

    # chart data
    try:
        subtitleText = 'the price chart'
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": r}
        xAxis = {"categories": dateList}
        yAxis = {"title": {"text": 'Price in dollars'}}
        pageType = 'graph'
    except:
        print('something went wrong with the highcart vars')

    return render_template("resultsLayout.html", pageType=pageType, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, imageUrl=imageUrl, sameCards = sameCards, cardId = cardId, sameCardsCombo = sameCardsCombo, cardInfo = cardInfo)

def searchCard(cardId, cur, priceList, dateList, imageUrl):
    # for the url I make the variable the string, and for the date and price I add them to the lists
    print('im doing a search card for:', cardId)
    try:
        for cardUrl in cur.execute("select PICURL from cards where id=\""+cardId+"\""):
            imageUrl = cardUrl[0]
            print('imageURL from searchcard:', imageUrl)
            # if the card is only foil, get foil prices. else get nonfoil prices
        for priceN in cur.execute("select datetime,normprice from prices where id=\""+cardId+"\" order by datetime asc"):
            priceList.append(priceN[1])
            dateList.append(priceN[0])
        return imageUrl
    except:
        print('the for-loops didnt work for cardUrl and price chart lists')

def updateTrend(cardId):
    print('running updateTrend for ',cardId)
    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()
    valueIndicator = ""
    valueIndicator = cardAverage.weekMonth(cardId)[2]
    # insert to watchlist
    try:
        cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)", (cardId, valueIndicator, ) )
        con.commit()
    except:
        print('could not update card with updateTrend')
    con.close()


@app.route('/search', methods=['GET'])
def searchGet():
    return render_template("searchGetLayout.html")

@app.route('/topCards')
def topCards():

    # this is too slow to run on every page load.
    # I need to do this daily and just import the json.
    """
    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT cards.NAME, cards.CARDSET, prices.FOILRATIO from prices, CARDS where NORMPRICE is not null and foilprice is not NULL and cards.ID = prices.ID order by datetime desc, FOILRATIO DESC limit 10")

    rows = cur.fetchall()
    for x in rows:
        print(x[0])
    con.close()
    """

    # tensorflow/keras processing could go here in the future
    
    # return render_template("topLayout.html", rows = rows)
    return render_template("topLayout.html")



def getWatchList():
    # this is a function to get the watchlist results which I use in my GET and POST for /watchlist
    con = sql.connect(dbLoc)
    con.row_factory = sql.Row
    cur = con.cursor()
    print('running getwatchlist')
    cur.execute("select cards.name, watchlist.pricedirection, cards.id from watchlist, cards where watchlist.id = cards.id")
    rows = cur.fetchall()

    for x in rows:
        print(x['id'])
    con.close()

    return rows


if __name__ == "__main__":
    app.run(debug=True)
