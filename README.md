# Mimicvat
This is an application to scrape and track Magic the Gathering card prices.

see it in action:
www.mimicvat.com

## Features
* bootstrap front-end
* SQL database back-end
* python web scrapers
* highcharts (javascript) price charts
* hosted online with a flask microframework on an Ubuntu server


## code breakdown
The main application file is project_flask.py. This contains the functions that control all interactions with the website like searching for cards, editing the watchlist, and displaying pages.
The html layouts for the site are in 'templates/', those are used by flask/jinja. 

The scraping is done with the file dailyTask.py, which is set up on the ubuntu server with cron to run at 6AM every day. This file calls other scrapers (which reside in 'scrapers/') and stores the values in a database called cardinfo.db (this database has to be built with dbSetup.py). The 'collections' feature tracks the percent of value gained from purchases, its the meat of the price tracking.
