import sqlite3

# run this once a day
# create db if not exists
def add_front_page():
    try:
        c.execute('''
        CREATE TABLE IF NOT EXISTS FRONTPAGE
        (DATETIME text,
        NORMPRICE real,
        UNIQUE(DATETIME))
        ''')
        print('added table to db')
    except:
        print('could not create table')

# collect all the prices for land tax and update db
def collect_prices():
    try:
        c.execute('select datetime,normprice from prices where id = "810a3792-a689-4849-bc14-fb3c71153aba"')
        rows = c.fetchall()
        for row in rows:
            print('adding',row)
            # put c execute here
            c.execute('insert or ignore into frontpage values (?,?)',(
                row[0],
                row[1]
            ))
    except:
        print('could not collect prices')

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

collect_prices()
c.execute('select * from frontpage')
rows = c.fetchall()
print('printing frontpage')
for row in rows:
    print(row)




cardsDb.commit()
cardsDb.close()
