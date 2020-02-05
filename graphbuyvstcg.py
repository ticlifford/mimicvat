from flask import Flask, render_template, request
import sqlite3 as sql
import cardAverage
import datetime as dt
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# this is a test file for graphing the tcg mid, buylist, and date on one chart




carddb = sql.connect("CARDINFO.db")
cursor = carddb.cursor()
cursor.execute('select buylist.DATETIME, buylist.BUYPRICE, prices.NORMPRICE from buylist, cardset,cards,prices where upper(cardset.NAME)= upper(replace(buylist.SETNAME,"-"," ")) and buylist.name = "Maze of Ith" and buylist.SETNAME = "eternal-masters" and cardset.code = cards.CARDSET and cards.NAME = buylist.NAME and prices.id = cards.ID and buylist.datetime=prices.DATETIME order by buylist.datetime')
rows = cursor.fetchall()
carddb.close()

datetime = []
buyprice = []
normprice = []

for row in rows:
    datetime.append(row[0])
    buyprice.append(row[1])
    normprice.append(row[2])
print(datetime)
dates_list = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in datetime]
print(dates_list)
#dates = pd.to_datetime(datetime, format="%Y%m%d")

#plt.plot(dates_list,buyprice,normprice)
plt.plot(dates_list,buyprice)
#plt.ylim(bottom=0)

plt.show()