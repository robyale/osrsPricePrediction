#!python
# -*- coding: utf-8 -*-

"""Gets Old School Runescape item and price
   data. Stores data in a local PostGres 
   Database.
"""
import datetime
import requests
import time
import requests
from bs4 import BeautifulSoup

__author__ = "Rob Yale"
__version__ = "1.0.0"
__status__ = "Prototype"

MILLISECONDS_DAY = 86400000

# Gets Old School Runescape items and GE price history
class fetch(object):
    # Gets todays date in milliseconds from epoch (1970/01/01)
    def getToday(self):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (datetime.datetime.today() - epoch).days * MILLISECONDS_DAY
    
    # Gets the largest item id
    # TODO change back to max when using entire data set
    # Currently min to use smaller data set
    def getMaxId(self):
        query = ("Select min(id) from public.items")
        return self.db.query(query)[0][0]
    
    # Get the last day prices were updated
    def getLastDay(self):
        lastDay = None
        if(self.maxID != None):
            query = ("Select max(day) from public.prices where item_id = " + str(self.maxID))
            lastDay = self.db.query(query)[0][0]
        return lastDay
    

    # Update database with all tradable items
    def updateItems(self):
        # Get id and name data from osrsbox.com
        url = ("https://www.osrsbox.com/osrsbox-db/items-complete.json")
        response = requests.get(url)
        data = response.json()
        
        # Get database ids
        query = ("Select id from public.items")
        ids = self.db.query(query)
        
        # Check for any new ids, and insert them into the database
        for item in data.keys():
            if(data[item]["tradeable_on_ge"] and not (any(data[item]["id"] in i for i in ids))):
                query = "INSERT INTO public.items (id, name) VALUES (%s,%s)"
                params = (data[item]["id"], data[item]["name"])
                self.db.insert(query, params)
               
    # Update price data for all tradable items
    # Depreciated, keeping for future reference
    # Initializing database would take multiple days
    def api(self):
        items = self.db.getItems()

        # OSRS API url
        root_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"
        json_ext = ".json"
    
        # Try to get price data for each tradable item
        for item, attribute in enumerate(items):
            itemID = items[item][0]
            url = root_url + str(itemID) + json_ext

            # Attempt to connect to OSRS API 6 times with increasing wait times
            for attempt in range(6):
                try:        
                    prices = requests.get(url).json()
                except:
                    print("Attempting reconnect", itemID, ": ", attempt)
                    time.sleep(attempt)
                else:
                    break
            else:
                raise ConnectionRefusedError("GE API refused to connect")

            # Insert price data into database
            for day in range(self.lastDay + MILLISECONDS_DAY, self.today, MILLISECONDS_DAY):
                query = "INSERT INTO public.prices (item_id, day, price) VALUES (%s, %s, %s)"
                params = (itemID, day, prices['daily'][str(day)])
                self.db.insert(query, params)
                
    def updateData(self):
        # Get the items to be updated
        items = self.db.getItems()
        names = [x[1] for x in items]#[item for t in items for item in t]
        names_formatted = [name.replace(" ", "_") for name in names]
        
        # URL to scrape from, initialize errors list
        base = "https://oldschool.runescape.wiki/w/Module:Exchange/"
        extension = "/Data"
        
        webErrors = []
        dataErrors = []
                        
        # Insert prices and volume for each name
        for i, name in enumerate(names):
            url = base + names_formatted[i] + extension
            print(name)
            
            # Try to connect
            try:
                response = requests.get(url)
                html = BeautifulSoup(response.content, 'html.parser')
                
                # Check if page returns data
                myID="Nothing_interesting_happens."
                if(html.find(id=myID) != None):
                    raise ConnectionError()
            except:
                webErrors.append(name)
                
            # If connected, add data to database
            else:
            # Scrape webpage for data, and add data
            # Data is in format 'day (milliseconds):price:volume'
                prices = [x.getText() for x in html.find_all("span", {"class", "s1"})]
                for price in prices:
                    temp = price.replace("'", "").split(":")
                    if(int(temp[0]) > self.lastDay):
                        # Try to insert data into database
                        try:
                            params = (items[i][0], int(temp[0]), int(temp[1]))
                            self.db.insertPrice(params)
                            # If there is volume information available, insert
                            if(len(temp) == 3):
                                params = (items[i][0], int(temp[0]), int(temp[2]))
                                self.db.insertVolume(params)
                        except:
                            dataErrors.append(name)
        print("Website errors:", webErrors)
        print("Data Errors:", dataErrors)

    # Check if the data needs updating
    def checkUpdate(self):
        if(self.today != (self.lastDay + MILLISECONDS_DAY)):
            return True
        else:
            return False
        
    # Update price/item data
    def update(self):
        if(self.checkUpdate()):
            # If it is Monday, update item data
            if(datetime.datetime.today().weekday() == 0):
                print("Updating Items!")
                start_time = time.time()
                self.updateItems()
                print("Updating items took: ", (time.time() - start_time), " seconds")
            
            # Update price data
            print("Updating Data!")
            start_time = time.time()
            self.updateData()
            print("Updating data took: ", (time.time() - start_time), " seconds")
    
    # Initialize database if there is no data
    # Warning: take a long time
    def initDatabase(self):
        print("Initializing database")
        start_time = time.time()
        # First day of GE data, - 1 to get data for first day too
        self.lastDay = 1427414400 - MILLISECONDS_DAY
        print("Inserting item data")
        self.updateItems()
        print("Inserting price and volume data")
        self.updateData()
        print("Initializing database took:", (time.time() - start_time), " seconds")
            
    # Initialize data fetcher
    def __init__(self, db):
        self.db = db
        self.today = self.getToday()
        self.maxID = self.getMaxId()
        if(self.maxID == None):
            self.initDatabase()
        else:
            self.lastDay = self.getLastDay()
            #self.update()

    