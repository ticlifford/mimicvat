import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv



#i'm going to swap out 'c18' for each set, there are about 30 of them
url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR10.TRC2.A0.H0.Xtithe.TRS2&_nkw=tithe&_sacat=0'

html = urllib.request.urlopen(url).read()

cardName = []
cardLabel = []

#print(html)
soup = b(html, 'html.parser')

s=soup.find('script')
print(soup)


"""
#there are a handful of script tags, and I want a certain one
#then I cut out some of the string to get it in dic format
scripts = soup.find_all('script')
dic = scripts[-3]
dic = str(dic)
cardDic = dic[26:-10]

cardDic = json.loads(cardDic)
oGdic = cardDic
cardDic = cardDic['cardlists']

"""