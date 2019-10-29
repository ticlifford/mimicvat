# Mimicvat
This is an application to scrape and track Magic the Gathering card prices.
## Features

* python web scrapers
* highcharts(javascript) price charts
* hosted online with a flask microframework
* bootstrap front-end

## see it in action
www.mimicvat.com

## code breakdown
the main application file is project_flask.py. This contains the functions that control all interactions with the website like searching for cards, editing the watchlist, and displaying pages.
The html layouts for the site are in templates/, those are used by flask/jinja. 
The scraping is done with the file dailyTask.py, which is set up on the ubuntu server with cron to run at 6AM every day. this file calls other scrapers(which reside in scrapers/) and store the values in a database called cardinfo.db (this database has to be built with dbSetup.py).