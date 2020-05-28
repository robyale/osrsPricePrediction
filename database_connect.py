#!python
# -*- coding: utf-8 -*-

"""Handles queries and other database related matters. 
"""
import psycopg2

USERNAME = 'postgres'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = '5432'
DBNAME = 'osrs_stocks'

__author__ = "Rob Yale"
__version__ = "1.0.0"
__status__ = "Prototype"

class MyDB(object):
    # Initialize database connection
    def __init__(self):
        self.connection = psycopg2.connect(user = USERNAME,
                                  password = PASSWORD,
                                  host = HOST,
                                  port = PORT,
                                  database = DBNAME)
        self.cursor = self.connection.cursor()

    # Queries database with query
    def query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    # Inserts items into database
    def insert(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        
    # Closes connections on exit
    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print("closed")
        
    # Insert a price into the table prices
    def insertPrice(self, params):
        query = "INSERT INTO public.prices (item_id, day, price) VALUES (%s, %s, %s)"
        self.insert(query, params)
        
    # Insert a volum into the table volume
    def insertVolume(self, params):
        query = "INSERT INTO public.volume (item_id, day, volume) VALUES (%s, %s, %s)"
        self.insert(query, params)
        
    # Get item data
    # TODO data is limited to 5 items for speed
    def getItems(self, id = None):
        if(id != None):
            query = ("Select * from public.items where id = " + str(id))
        else:
            query = ("Select * from public.items")# LIMIT 5")
        return self.query(query)
        
    # Returns item price data
    def getPrices(self, id = None):
        if(id != None):
            query = ("Select * from public.prices where item_id = " + str(id))
        else:
            query = ("Select * from public.prices")
        return self.query(query)
        
    # Returns item volume data
    def getVolume(self, id = None):
        if(id != None):
            query = ("Select * from public.volume where item_id = " + str(id))
        else:
            query = ("Select * from public.volume")
        return self.query(query)
        
        
        