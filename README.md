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

## How to get this running
*First, initiate the database by running dbsetup.py. This creates a database file called cardinfo.db.
*Next, you will need to schedule the scrapers. dailyTask.py needs to be set to run(daily) to scrape prices.
*You will also need to schedule setcardscraper.py to run every month or so to collect the new cards.
*Finally, to boot up the flask application you just run project_flask.py.
*At this point you can access the app by going to localhost:5000 in your browser.
