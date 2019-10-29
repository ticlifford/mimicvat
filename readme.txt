Timothy Clifford
Magic card price tracker
5/9/19

---starting the application---
My final project is run by final_project_flask.py. It is accessed by flask's normal localhost:5000.

I included the database file called CARDINFO.db which should be fine to view the application and try it out.
I created that database by running dbSetup.py and then running some scrapers. The way the scrapers work 
is by first running setNameCollector.py, then setPriceScraper.py and setCardScraper.py.
IMPORTANT to note, is that setNameCollector.py really does collect ALL sets, which is a lot. it collects around 500 sets.
Running other scrapers after that takes way more time, because they go through each set that is in the setNames.csv
For simplicity, I edited the setNames.csv to only have one set, so you can test out setPriceScraper.py or setCardScraper.py easily.

Other scrapers:
I have a working scraper called edhrecScraper.py which uses BeautifulSoup. It works fine, but the data I collected with it 
has not been used in this project so far, because it is for predictive features. It may be useful in the future but isn't displayed yet.

ebayScraper.py is a work in progress, I think it would be interesting to scrape ebay for the number of specific cards for sale,
and average price. This is also for a future feature.

templates folder:
these are all my flask templates. For the most part, they all inherit layout.html and use the normal jinja templating stuff.
The layout has bootstrap on it so it looks nice.

other files:
cardAverage.py is the file to compare average prices. It is called when necessary by the main application.
It takes the statistical standard deviation of the past 30 days and average, and today's price, to figure out the monthly
trend (price went up, price went down, price stayed the same). It does the same thing with the weekly price. Since it does
this daily, I compare the two. If the price trend changes it's direction, the pricetrend variable changes, which is displayed
in the watchlist. 

Important to note, is that since I'm using the statistics package I need at least two numbers to do the math with.
This means obviously, the FIRST time a card's price is logged I don't have a second number to do any math with and it returns
something like "I don't know what's happening with the price"

Similarly, most of the cards don't have tons of price data simply because I just finished this program and haven't been running
the price scraper long. This means most cards have a flat graph when you use the search feature.

In a real application of this project, the setPriceScraper.py would be a scheduled task that is run every day. As an example
on a ubuntu server I would use something like "cron" to schedule a bash script that reads:
02 4 * * * /etc/setPriceScraper.py