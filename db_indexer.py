import sqlite3

cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()
try:
    c.execute('create index card_id_idx on prices (id);')
    print('indexed id in prices table')
except:
    print('could not index id in prices table')

cardsDb.commit()
cardsDb.close()