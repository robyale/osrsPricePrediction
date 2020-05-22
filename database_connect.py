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