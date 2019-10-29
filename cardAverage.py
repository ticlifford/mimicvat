
#this program takes in a card ID, calculates the average past 7 days, and calculates the standard deviation
#it does the same with the past month
#if the currrent day's price falls outside this standard deviation, It prints it accordingly
#it also compares the month and week trends to track CHANGES in the direction which is a big indicator for buying and selling

# importing Statistics module 
import statistics 
import time
import datetime
import sqlite3

#chart stuff
#import matplotlib.pyplot as plt
#import numpy as np

#dbLoc = '/home/timc/flask_project/flask_app/CARDINFO.db'
dbLoc = 'CARDINFO.db'




#open card database
#cardsDb = sqlite3.connect('CARDINFO.db')
#c = cardsDb.cursor()


def checkPriceMonth(cardId):
    #print('the card ID is',cardId)


    #db
    cardsDb = sqlite3.connect(dbLoc)
    #cardsDb = sqlite3.connect('CARDINFO.db')
    c = cardsDb.cursor()
    #list variables
    normL = []
    foilL = []
    current = []

    #loop that makes lists of the price for the month
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 30',(cardId,)):
    #for row in c.execute('SELECT * from PRICES GROUP BY NORMPRICE ORDER BY max(timestamp) desc WHERE ID =' + '\'' + cardId + '\''): ORDER BY max(timestamp) desc
        #just prints date stamp
        normL.append(row[2])
        foilL.append(row[3])
        #print(row)

    #loop that selects today's prices
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 1',(cardId,)):
        current.append(row[2])
        current.append(row[3])
    try:
        foilMulti = current[1]/current[0]
        #print('the foil multiplier is:',foilMulti)
    except:
        print('could not compute foil multiplier')

#month averages for normal and foil prices
    try:
        normMean = statistics.mean(normL)
        foilMean = statistics.mean(foilL)
    except:
        print('could not find means')

#month standard D
    try:
        normDev = statistics.stdev(normL)
    except:
        print('cant find standard dev for month')
    #print(normDev)

    #close db
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

def checkPriceWeek(cardId):
    #print('the card ID is',cardId)

    #db
    cardsDb = sqlite3.connect(dbLoc)
    #cardsDb = sqlite3.connect('CARDINFO.db')
    c = cardsDb.cursor()

    #list variables
    normL = []
    foilL = []
    current = []

    #loop that makes week lists
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 7',(cardId,)):
    #for row in c.execute('SELECT * from PRICES GROUP BY NORMPRICE ORDER BY max(timestamp) desc WHERE ID =' + '\'' + cardId + '\''): ORDER BY max(timestamp) desc
        #just prints date stamp
        normL.append(row[2])
        foilL.append(row[3])
        #print(row)

    #loop that selects today's prices
    for row in c.execute('select * from PRICES  where ID = ? ORDER BY datetime DESC LIMIT 1',(cardId,)):
        current.append(row[2])
        current.append(row[3])
    try:
        foilMulti = current[1]/current[0]
        #print('the foil multiplier is:',foilMulti)
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
#week standard D
    try:
        normDev = statistics.stdev(normL)
    except:
        print('no normal standard dev')
    #print(normDev)

    #close db
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

def weekMonth(ID):
    #initializing variables
    
    returnList = []
    week = checkPriceWeek(ID)
    month = checkPriceMonth(ID)
    returnList.append(week)
    returnList.append(month)

#this is a big if statement to determine the action that is presented in the watchlist
#I take the monthly trend and compare it to the weekly trend. If the trends are not the same, then the price has changed direction and this is important to know

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






#print(weekMonth('e1a4e33f-53f0-4919-98a1-c832dcd32efb'))
