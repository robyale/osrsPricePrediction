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
class scraper(object):
    # Gets todays date in milliseconds from epoch (1970/01/01)
    def getToday(self):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (datetime.datetime.today() - epoch).days * MILLISECONDS_DAY
    
    # Gets the largest item id
    def getMaxId(self):
        # TODO change min to max when data set up
        query = ("Select min(id) from public.items")
        return self.db.query(query)[0][0]
    
    # Get the last day prices were updated
    def getLastDay(self):
        query = ("Select max(day) from public.prices where item_id = " + str(self.maxID))
        return self.db.query(query)[0][0]
    
    # Check if the data needs updating
    def needUpdate(self):
        if(self.today != (self.lastDay + MILLISECONDS_DAY)):
            return True
        else:
            return False

    # Get all tradable items
    def updateItems(self):
        url = ("https://www.osrsbox.com/osrsbox-db/items-complete.json")
        response = requests.get(url)
        data = response.json()
        query = ("Select id from public.items")
        ids = self.db.query(query)
        
        for item in data.keys():
            if(data[item]["tradeable_on_ge"] and not (any(data[item]["id"] in i for i in ids))):
                query = "INSERT INTO public.items (id, name) VALUES (%s,%s)"
                params = (data[item]["id"], data[item]["name"])
                self.db.insert(query, params)

    # Update price/item data
    def update(self):
        if(self.needUpdate()):
            if(datetime.datetime.today().weekday() == 0):
                print("Updating Items!")
                start_time = time.time()
                self.updateItems()
                print("Updating items took: ", (time.time() - start_time), " seconds")

            print("Updating Data!")
            start_time = time.time()
            query = ("Select * from public.items ORDER BY id ASC LIMIT 5")
            items = self.db.query(query)
            print(items)

            root_url = "http://services.runescape.com/m=itemdb_oldschool/api/graph/"
            json_ext = ".json"
        
            for item, attribute in enumerate(items):
                itemID = items[item][0]
                url = root_url + str(itemID) + json_ext
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
                for day in range(self.lastDay + MILLISECONDS_DAY, self.today, MILLISECONDS_DAY):
                    query = "INSERT INTO public.prices (item_id, day, price) VALUES (%s, %s, %s)"
                    params = (itemID, day, prices['daily'][str(day)])
                    self.db.insert(query, params)
                    
            print("Updating data took: ", (time.time() - start_time), " seconds")

    def __init__(self, db):
        self.db = db
        self.today = self.getToday()
        self.maxID = self.getMaxId()
        self.lastDay = self.getLastDay()
        self.update()

    # Returns item price data
    def getPrices(self, id):
        if(id != None):
            query = ("Select * from public.prices where item_id = " + str(id))
        else:
            query = ("Select * from public.prices")
        return self.db.query(query)
    
    # Returns item name and id
    def getItems(self, id):
        if(id != None):
            query = ("Select * from public.items where id = " + str(id))
        else:
            query = ("Select * from public.items")
        return self.db.query(query)

