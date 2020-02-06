
#this program takes in a card ID, calculates the average past 7 days and calculates the standard deviation
#it does the same with the past month
#if the currrent day's price falls outside this standard deviation, It prints it accordingly
#it also compares the month and week trends to track CHANGES in the direction which is a big indicator for buying and selling

import statistics 
import time
import datetime
import sqlite3

dbLoc = '/home/timc/flask_project/flask_app/CARDINFO.db'
#dbLoc = 'CARDINFO.db'

def checkPriceMonth(cardId):
    cardsDb = sqlite3.connect(dbLoc)
    c = cardsDb.cursor()
    normL = []
    foilL = []
    current = []

    # prices for 30 days
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 30',(cardId,)):
        normL.append(row[2])
        foilL.append(row[3])

    #prices for most recent day
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 1',(cardId,)):
        current.append(row[2])
        current.append(row[3])

    try:
        foilMulti = current[1]/current[0]
    except:
        print('could not compute foil multiplier')

    try:
        normMean = statistics.mean(normL)
        foilMean = statistics.mean(foilL)
    except:
        print('could not find means')

#monthly standard dev
    try:
        normDev = statistics.stdev(normL)
    except:
        print('cant find standard dev for month')

    cardsDb.close()

#price check
    try:
        if current[0] > normMean+normDev:
            return 'the value is going up this month'
            #trigger an email
        elif current[0] < normMean - normDev:
            return 'the value is going down this month'
        else:
            return 'the price has not changed appreciably this month'
    except:
        print('could not do month value change')
        return 'could not do month value change'

def checkPriceWeek(cardId):
    cardsDb = sqlite3.connect(dbLoc)
    c = cardsDb.cursor()

    normL = []
    foilL = []
    current = []

    for row in c.execute('select * from PRICES where ID = ? ORDER BY datetime DESC LIMIT 7',(cardId,)):
        normL.append(row[2])
        foilL.append(row[3])

    for row in c.execute('select * from PRICES where ID = ? ORDER BY datetime DESC LIMIT 1',(cardId,)):
        current.append(row[2])
        current.append(row[3])
    try:
        foilMulti = current[1]/current[0]
    except:
        print('could not do foil multiplier')

#week averages for normal and foil prices
    try:
        normMean = statistics.mean(normL)
    except:
        print('no normal mean')
    try:
        foilMean = statistics.mean(foilL)
    except:
        print('no foil mean')

    try:
        normDev = statistics.stdev(normL)
    except:
        print('no normal standard dev')

    cardsDb.close()

#price check
    try:
        if current[0] > normMean+normDev:
            return 'the value is going up this week'
            #trigger an email
        elif current[0] < normMean - normDev:
            return 'the value is going down this week'
        else:
            return 'the price has not changed appreciably this week'
    except:
        print('could not find weekly value change')
        return 'could not find weekly value change'

def weekMonth(ID):
    #this is a big if statement to determine the action that is presented in the watchlist
    #I take the monthly trend and compare it to the weekly trend. If the trends are not the same,
    # then the price has changed direction and this is important to know

    returnList = []
    week = checkPriceWeek(ID)
    month = checkPriceMonth(ID)
    returnList.append(week)
    returnList.append(month)

    if month=='the value is going down this month' and week=='the value is going up this week':
        returnList.append("you should definitely buy")
    elif month=='the value is going down this month' and week=='the price has not changed appreciably this week':
        returnList.append("you should probably buy")
    elif month=='the value is going down this month' and week=='the value is going down this week':
        returnList.append("the price is still going down, do not buy")

    elif month=='the value is going up this month' and week=='the value is going up this week':
        returnList.append("the price continues to climb. You should buy only if you need it")
    elif month=='the value is going up this month' and week=='the value is going down this week':
        returnList.append("the price may crash. Don't buy, and sell if you have it")
    elif month=='the value is going up this month' and week=='the price has not changed appreciably this week':
        returnList.append("the price is in a plateau")

    elif month=='the price has not changed appreciably this month' and week=='the value is going up this week':
        returnList.append("the price is rising, you should buy")
    elif month=='the price has not changed appreciably this month' and week=='the price has not changed appreciably this week':
        returnList.append("the price has not moved at all, you may as well sell or buy")
    elif month=='the price has not changed appreciably this month' and week=='the value is going down this week':
        returnList.append("the price is dipping. Sell now, do not buy")
    else:
        returnList.append("I do not know whats happening with this card")

    return returnList