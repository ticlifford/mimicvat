import sqlite3
import matplotlib.pyplot as plt


# this script is for compiling a list of dates:total collection value
# I build a dictionary and run through a list of IDs (placeholder is collection_list)
# I am left with collection_dic and can pass that to highcharts

def compile_collection(collection_list):
    #collection_list = ['asdfasdf','werwerwerwe','fjfjsdijfjid']

    collection_dic = {}

    # goes through collection and compiles a total value by datetime
    # I should strip the hour and minute timecode from series data
    for card_id in collection_list:
        price_info = cursor.execute('select * from prices where id=?',(card_id,))
        
        for row in price_info:
            #print(row)
            if row[0] in collection_dic:
                collection_dic[row[1]] +=  row[2]
                print('adding ',row)
            else:
                collection_dic[row[1]] = row[2]
    return collection_dic


collection_list = ['856f804d-0213-4b86-bc6a-6a0a1147c4f9',
                    'fd8ccd81-9e11-47fa-8e16-064c52c24506',
                    'eeca4557-98aa-433b-a3ee-050e4a3e6d88']

#connect to db here
cardsDb = sqlite3.connect('CARDINFO.db')
cursor = cardsDb.cursor()

#collection compiler runs here
col_dic = compile_collection(collection_list)

#close connection to db here
cardsDb.close()

#print(col_dic)
#plt.plot(col_dic)
print('plotting')
plt.plot(list(col_dic.keys()),list(col_dic.values()))
plt.ylabel('value')
plt.xlabel('time')
plt.show()
print('finished plotting')

# i've structured this to build a graph of the historical prices

# in practice, each user will start with nothing, and their db will
# grow as they add cards

# I need a db with these values:
# user_id
# datetime
# market_value
# paid_value
# number_owned

# run daily:
"""
daily_total = 0
for card in collection_list:
    card_val = cursor.execute('select normprice from prices where id =? and datetime=?',(card_id,datetime,))
    daily_total =+ card_val
cursor.execute('insert user_id,daily_total,datetime into card_collection')
"""