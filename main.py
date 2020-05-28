#!python
# -*- coding: utf-8 -*-
#%%

"""Runs modules to retreive and update
    Old School Runescape item and price 
    information in a local database. Predicts 
    future GE prices with LSTM model.
"""
import numpy as np
#from data import fetch
import data
import matplotlib.pyplot as plt
import database_connect
import statistics as st
from model import model
import time

__author__ = "Rob Yale"
__version__ = "1.0.0"
__status__ = "Prototype"


db = database_connect.MyDB()

# Print PostgreSQL Connection properties
print (db.connection.get_dsn_parameters(),"\n")
blacklist = []


# Get stock prices
data = data.fetch(db)
# Get list of ids
query = "SELECT DISTINCT item_id FROM public.prices LIMIT 1"
idTuples = db.query(query)
ids = [item for t in idTuples for item in t]
#%%

numDays = 22
numSamples = 5
means = {}
std = {}

start_time = time.time()
for id in ids:
    priceTuples = db.getPrices(id)
    
    # Get day and price
    x_val = [x[2]/86400000 for x in priceTuples]
    y_val = [x[3] for x in priceTuples]
    
    # Set up training data
    prices = [[el] for el in np.array(y_val)]
    myModel = model(prices, numDays)
    #myModel.plotData()
    RMSE = []
    for i in range(numSamples):
        predictions, rmse = myModel.predictModel()
        RMSE.append(rmse)
    means[id] = st.mean(RMSE)
    std[id] = st.pstdev(RMSE)
    
print(time.time() - start_time)
print(means)
print(std)






    
    
    
