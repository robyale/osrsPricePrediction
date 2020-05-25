#!python
# -*- coding: utf-8 -*-

"""Gets Old School Runescape item and price
   data. Stores data in a local PostGres 
   Database.
"""
import datetime
import requests
import time

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
    def updateData(self):
        # Get all item ids (currently limited to 5 items for speed)
        query = ("Select * from public.items ORDER BY id ASC LIMIT 5")
        items = self.db.query(query)

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
    def initDatabase(self):
        print("Initializing database")
        start_time = time.time()
        self.lastDay = self.today - (179 * MILLISECONDS_DAY)
        self.updateItems()
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
            self.update()

    # Returns item price data
    def getPrices(self, id = None):
        if(id != None):
            query = ("Select * from public.prices where item_id = " + str(id))
        else:
            query = ("Select * from public.prices")
        return self.db.query(query)
    
    # Returns item name and id
    def getItems(self, id = None):
        if(id != None):
            query = ("Select * from public.items where id = " + str(id))
        else:
            query = ("Select * from public.items")
        return self.db.query(query)