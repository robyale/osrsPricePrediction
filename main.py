#!python
# -*- coding: utf-8 -*-

"""Runs modules to retreive and update
    Old School Runescape item and price 
    information in a local database. Predicts 
    future GE prices with LSTM model.
"""
import numpy as np
import datascrape
import matplotlib.pyplot as plt
import database_connect
from model import model

__author__ = "Rob Yale"
__version__ = "1.0.0"
__status__ = "Prototype"

# Connect to database using database_connect.py module
db = database_connect.MyDB()

# Print PostgreSQL Connection properties
print (db.connection.get_dsn_parameters(),"\n")


# Get stock prices
data = datascrape.scraper(db)
prices = data.getPrices('2')

# Get day and price
x_val = [x[2]/86400000 for x in prices]
y_val = [x[3] for x in prices]

# Set up training data
numDays = 22
data = [[el] for el in np.array(y_val)]
myModel = model(data, numDays)
myModel.plotData()
