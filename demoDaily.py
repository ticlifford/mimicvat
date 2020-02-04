#!/usr/bin/python3
"""
crontest for daily
"""
import os 
import project_flask
import datetime
import time


print('running dailytask')
fPath = '/home/timc/flask_project/flask_app/daily.txt'
# get the date

try:
    with open(fPath, 'a') as f:
    #with open('daily.txt', 'a') as f:
        f.write('\n demo edited')
    print('wrote to daily.txt')
except:
    print('could not write to daily.txt')