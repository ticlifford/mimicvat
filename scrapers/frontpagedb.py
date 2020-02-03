import sqlite3

dbpath = '/home/timc/flask_project/flask_app/CARDINFO.db'

# collect all the prices for land tax and update db
def collect_prices():
    try:
        c.execute('select datetime,normprice from prices where id = "810a3792-a689-4849-bc14-fb3c71153aba" order by datetime desc')
        row = c.fetchone()
        print('adding:',row)
        c.execute('insert or ignore into frontpage values (?,?)',(
            row[0],
            row[1]
        ))
        print('finished frontpage insert')
    except:
        print('could not collect prices')

cardsDb = sqlite3.connect(dbpath)
c = cardsDb.cursor()

collect_prices()

cardsDb.commit()
cardsDb.close()
