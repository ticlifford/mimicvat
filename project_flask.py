from flask import Flask, render_template, request
import sqlite3 as sql
import cardAverage


# This is my flask file which runs the application

app = Flask(__name__)

# for adjusting the location of the database, when running locally vs on server
#dbLoc = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbLoc = 'CARDINFO.db'

# App routes

# the front page with bootstrap layout parent
@app.route('/')
def index(chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):
    
    # static variables for Land Tax (example on front page)
    priceList = []
    dateList = []
    cardId = "810a3792-a689-4849-bc14-fb3c71153aba"
    imageUrl = ""
    #imageUrl = "https://img.scryfall.com/cards/normal/front/8/1/810a3792-a689-4849-bc14-fb3c71153aba.jpg?1562920975"
    cardName = "Land Tax"


    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)

    # chart stuff

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

# list page using bootstrap layout parent
@app.route('/list')
def listPage():

    # database stuff collecting all cards
    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from CARDS where cardset='aer'")
    rows = cur.fetchall()
    con.close()

    return render_template("listLayout.html", rows = rows)

# watchlist
@app.route('/watchlist', methods=['POST', 'GET'])
def watchlist():

    # get request to display the card watchlist
    if request.method == 'GET':
        print('watchlist get request')
        rows = getWatchList()



        return render_template("watchlistLayout.html", rows = rows)

    # Post request to add to the watchlist
    elif request.form.get('removeCard') == None:
        print('/watchlist post request insert')
        con = sql.connect("CARDINFO.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        r = (request.form['watchlist'])

        # initialized variables
        cardId = ""
        valueIndicator = ""
        # get the ID of the card i'm adding
        try:
            for cardIdNum in cur.execute("select ID from CARDS where UPPER(NAME)=UPPER((?))", (r, )):
                cardId = cardIdNum[0]
        except:
            print('could not find card')

        # gets the cardAverage week/month for the searched card
        valueIndicator = cardAverage.weekMonth(cardId)[2]


        # insert to watchlist
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)", (cardId, valueIndicator, ) )
            con.commit()
            con.close()
        except:
            print('could not insert card')

        # displaying watchlist
        """
        cur.execute("with datetim as (select normprice, prices.id, datetime from prices order by datetime desc ) select normprice, watchlist.ID as id, name, pricedirection from datetim, watchlist, cards where watchlist.id = datetim.id and cards.id = watchlist.id group by watchlist.id")
        rows = cur.fetchall()
        con.close()
        """
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows=rows)

    # post request to remove card from list
    else:
        print("remove card post request")
        # database stuff
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

        # displaying watchlist
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows = rows)

# the search bar results for the layout html

@app.route('/search/<cardId>', methods=['GET', 'POST'])
def searchID(cardId, chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):

    # this is the search bar, i'm not using it I think
    # r = (request.form['searchbar'])
    if request.method == "GET":
        print('search cardID get request')
        # connecting to db
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
            # print(cur.fetchone(), namie)
            # print(cur.fetchone())
            # sameCards.append(cardIdNum[0])
        except:
            print('I couldnt get the card name')


        # select ids of all reprints

        print('card im looking up:', cardId)
        # make sure I didn't make a mess of this. i'm trying to make a new list called samecardscombo that has both the ids and sets of alternate cards. try x,y.
        # it didn't work the first time because I didn't have a complete database to search through but I'm running the card scraper now.

        # this works, and should be put into a function to call in this and the other search method, and passed to the render


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
                # print('id:', cardId)
                print("x 0:",x[0])
                print("x 1:",x[1])
            print('samecardcombo:',sameCardsCombo)

        except:
            print('I couldnt select the ids for samecards')


        try:
            imageUrl = searchCard(cardId, cur, priceList, dateList, imageUrl)
        except:
            print('cant perform searchcard')
        # print('imageUrl after searchcard:', imageUrl)
        cur.execute("select cards.cmc, type, power, toughness, rarity from cards where cards.id == ((?))",(cardId, ))
        #cur.execute("select cards.cmc, cards.type, cards.power, cards.toughness, cards.rarity, buylist.datetime, replace(buylist.setname,'-',' ') as nohyphen, BUYLIST.BUYPRICE, cards.ID from buylist, cardset, cards where upper(nohyphen) = upper(cardset.name) and upper(cardset.code) = upper(cards.cardset) and cards.name = buylist.NAME  and cards.id == ((?)) order by buylist.DATETIME desc",(cardId, ))
        fetchInfo = cur.fetchone()
        for value in fetchInfo:
            print('value: ',value)
        try:
            cardInfo['cmc'] = fetchInfo[0]
            cardInfo['type'] = fetchInfo[1]
            cardInfo['power'] = fetchInfo[2]
            cardInfo['toughness'] = fetchInfo[3]
            cardInfo['rarity'] = fetchInfo[4]
            #cardInfo['buylist'] = fetchInfo[7]
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
        #print('buylist: ',cardInfo['buylist'])

        
        # I close the db
        con.close()

        # the chart goes here
        subtitleText = 'the price chart'
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": 'x'}
        series = [{"name": 'Price', "data": priceList}]
        title = {"text": cardName}
        xAxis = {"categories": dateList}
        yAxis = {"title": {"text": 'Price in dollars'}}
        pageType = 'graph'

        # the render goes here
        return render_template("resultsLayout.html", pageType=pageType, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, imageUrl=imageUrl, sameCards = sameCards, setCodes = setCodes, cardId = cardId, sameCardsCombo = sameCardsCombo, cardInfo = cardInfo)

    # post means i'm adding a card to the watchlist
    elif request.method == "POST":
        print('the request was post')

        con = sql.connect("CARDINFO.db")
        cur = con.cursor()

        valueIndicator = cardAverage.weekMonth(cardId)[2]
        # insert to watchlist
        try:
            cur.execute("INSERT or replace into watchlist (ID, PRICEDIRECTION) values (?, ?)", (cardId, valueIndicator, ) )
            con.commit()
        except:
            print('could not insert card')
        con.close()
        rows = getWatchList()

        return render_template("watchlistLayout.html", rows = rows)



# the 404 page function

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# function to search with the searchbar form result

@app.route('/search', methods=['POST'])
def searchResults(chartID = 'chart_ID2', chart_type = 'line', chart_height = 500):

    print('doing search post method')
    if request.form.get('searchbar') == None:
        print("request form searchbar is nothing:", request.form.get('addCard'))
        return "searchbar is nothing"
    else:
        print('request form searchbar has a value')

    # r is a string containing the name of what I'm searching for
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
    # connecting to db
    con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # initializing my variables, cardId as a string, pricelist/datelist for graph, imageurl as string, cardInfo as dictionary
    cardId = ""
    priceList = []
    dateList = []
    imageUrl = ""
    cardInfo = {}

    sameCards = []
    sameCardsCombo = []
    # for the result of the name search, get the ID and put it in cardId, then print it
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
                
            print("i found an ID")
            # print('id:', cardId)
            print("x 0:",x[0])
            print("x 1:",x[1])
        print('samecardcombo:',sameCardsCombo)

    except:
        print('I couldnt select the ids for samecards')
        # return a "could not find" page here

    try:
        for cardIdNum in cur.execute("select ID, CARDSET from CARDS where UPPER(NAME)=UPPER((?))", (r, )):
            cardId = cardIdNum[0]

            # most cards have more than one printing, this compiles a list of each card
            # currently, I display the last card that's in my list which is pretty random
            sameCards.append(cardIdNum[0])

            # inside this loop I should also grab the set code to display on the search page with each ID
            # in the html ill do an a href link to that page, I will need to redesign the search results flask URL though.
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
    # I close the db
    

    # here I collect the bits of data I want to display, cmc, color, stats etc
    # I will need to do this in a function so I can place it in both search methods
    cur.execute("select cards.cmc, type, power, toughness, rarity from cards where cards.id == ((?))",(cardId, ))
    #cur.execute("select cards.cmc, cards.type, cards.power, cards.toughness, cards.rarity, buylist.datetime, replace(buylist.setname,'-',' ') as nohyphen, BUYLIST.BUYPRICE, cards.ID from buylist, cardset, cards where upper(nohyphen) = upper(cardset.name) and upper(cardset.code) = upper(cards.cardset) and cards.name = buylist.NAME  and cards.id == ((?)) order by buylist.DATETIME desc",(cardId, ))
    fetchInfo = cur.fetchone()
    for value in fetchInfo:
        print('value: ',value)
    try:
        cardInfo['cmc'] = fetchInfo[0]
        cardInfo['type'] = fetchInfo[1]
        cardInfo['power'] = fetchInfo[2]
        cardInfo['toughness'] = fetchInfo[3]
        cardInfo['rarity'] = fetchInfo[4]
        #cardInfo['buylist'] = fetchInfo[7]
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
    #print('buylist: ',cardInfo['buylist'])

    #print('the card type:', cardInfo['type'][1])
    con.close()
    # the chart goes here

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

    # the render goes here
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
        
        # I could insert another for loop to collect buylist here
        """
        for buyPriceN in cur.execute("select")
        """

        return imageUrl
    except:
        print('the for loops didnt work for cardUrl and price chart lists')

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

    # cur.execute("with datetim as (select normprice, prices.id, datetime from prices order by datetime desc ) select normprice, watchlist.ID as id, name, pricedirection from datetim, watchlist, cards where watchlist.id = datetim.id and cards.id = watchlist.id group by watchlist.id")
    # `rows = cur.fetchall()
    con.close()


@app.route('/search', methods=['GET'])
def searchGet():
    return render_template("searchGetLayout.html")

@app.route('/topCards')
def topCards():


    con = sql.connect(dbLoc)
    #con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT cards.NAME, cards.CARDSET, prices.FOILRATIO from prices, CARDS where NORMPRICE is not null and foilprice is not NULL and cards.ID = prices.ID order by datetime desc, FOILRATIO DESC limit 10")

    rows = cur.fetchall()
    for x in rows:
        print(x[0])
    con.close()
    # put a function here that gets buy/sell ratios

    #cur.execute("") # buy/sell ratio

    """
    select cards.name, cards.ID, prices.NORMPRICE, buylist.BUYPRICE, BUYPRICE/NORMPRICE as buy_ratio
 from cards, prices, buylist, cardset
 where cards.CARDSET = cardset.CODE
 and buylist.SETNAME = upper(CARDSET.NAME)
 and buylist.NAME = cards.NAME
 and cards.id = prices.ID
 and BUYLIST.DATETIME = "2019-08-10"
 and PRICES.DATETIME = "2019-08-10"
 order by buy_ratio DESC
    """

    # tensorflow/keras processing

 

    return render_template("topLayout.html", rows = rows)


# this is a function to get the watchlist results which I use in my GET and POST for /watchlist
def getWatchList():
    con = sql.connect(dbLoc)
    # con = sql.connect("CARDINFO.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    print('running getwatchlist')

    # this search seems to be slow, and makes the page loading a problem
    # this search gets the all the data from watchlist, then adds the name from cards and the most recent price from prices
    # the trouble is that the subquery to get normprice from prices is too slow
    # can normprice be added to the watchlist update? this would be more performant while being technically inefficient database design (normal form)
    
    #cur.execute("with datetim as (select normprice, prices.id, datetime from prices order by datetime desc ) select normprice, watchlist.ID as id, name, pricedirection from datetim, watchlist, cards where watchlist.id = datetim.id and cards.id = watchlist.id group by watchlist.id")
    cur.execute("select cards.name, watchlist.pricedirection, cards.id from watchlist, cards where watchlist.id = cards.id")

    rows = cur.fetchall()

    
    for x in rows:
        print(x['id'])
    
    con.close()

    # alternatively, I may be able to (select * from watchlist) then (select normprice, name from prices, cards, watchlist where id=id=id order desc group by 1)
    return rows

# Flask thing to run the app
if __name__ == "__main__":
    app.run(debug=True)

