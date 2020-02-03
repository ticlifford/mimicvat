import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys

fPath = '/home/timc/flask_project/flask_app/daily.txt'
csvPath = '/home/timc/flask_project/flask_app/setNames.csv'

with open(csvPath, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        try:
            print(line[0])
        except:
            print('could not print line')