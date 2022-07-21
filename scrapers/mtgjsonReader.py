import ujson

try:
    all_prices = 'C:/Users/Tim/Downloads/AllPrices.json'

    f = open(all_prices)

    data = ujson.load(f)

    print(next(iter(data[0])))

except:
    print('error in json')
print('finished')