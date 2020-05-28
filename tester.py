# -*- coding: utf-8 -*-
#%%
"""
Created on Mon May 25 16:14:44 2020

@author: Rob
"""
import database_connect
import numpy as np
import time
import requests
from bs4 import BeautifulSoup
from model import model
import statistics as st

#%%

db = database_connect.MyDB()

query = "Select name from public.items ORDER BY id ASC LIMIT 19"
items = db.query(query)
items = [item for t in items for item in t]
names = [item.replace(" ", "_") for item in items]
print(items)

#%%
db = database_connect.MyDB()

query = "Select name from public.items ORDER BY id ASC LIMIT 100"
items = db.query(query)
items = [item for t in items for item in t]
names = [item.replace(" ", "_") for item in items]

webErrors = []
dataErrors = []
myTimes = []
base = "https://oldschool.runescape.wiki/w/Module:Exchange/"
extension = "/Data"
                
start_time = time.time()
# Insert prices and volume for each name
for j in range(5):
    for i, name in enumerate(names):
        # Build url for item
        url = base + names[i] + extension
        print(name)
        
        # Try to connect
        try:
            response = requests.get(url)
            html = BeautifulSoup(response.content, 'html.parser')
            
            # Check if page returns data
            myID="Nothing_interesting_happens."
            if(html.find(id=myID) == None):
                raise ConnectionError()
        except:
            webErrors.append(name)
    myTime = time.time() - start_time
    myTimes.append(myTime)
print(st.mean(myTimes))




# name = "Shantay pass"
# url = base + name + extension
# response = requests.get(url)
# html = BeautifulSoup(response.content, 'html.parser')
# myID="Nothing_interesting_happens."
# errorcode = html.find(id=myID)
# #errorcode = html.find("span", {"class", "s1"})
# print(errorcode)
# print(name in str(html.title))
# print(str(html.title))



#%%
base = "https://oldschool.runescape.wiki/w/Module:Exchange/"
extension = "/Data"
history = {}
webErrors = []
start_time = time.time()
for i, name in enumerate(names):
    localHistory = {}
    url = base + name + extension
    print(items[i])
    try:
        response = requests.get(url)
    except:
        webErrors.append(items[i])
    else:
        soup = BeautifulSoup(response.content, 'html5lib')
        prices = [x.getText() for x in soup.find_all("span", {"class", "s1"})]
        for price in prices:
            temp = price.replace("'", "").split(":")
            localHistory[int(temp[0])] = int(temp[1])
        
        history[items[i]] = localHistory
print(webErrors)
print(time.time() - start_time)
#%%
prices = [[el] for el in np.array(list(localHistory.values()))]
myModel = model(prices, 22)
prediction, rmse = myModel.predictModel()

#%%
myModel.plotData(prediction)

#%%
db = database_connect.MyDB()

query = "Select * from public.items ORDER BY id ASC LIMIT 1"
items = db.query(query)
names = [x[1] for x in items]
names_formatted = [name.replace(" ", "_") for name in names]


base = "https://oldschool.runescape.wiki/w/Module:Exchange/"
extension = "/Data"
history = {}
volume = {}
webErrors = []
start_time = time.time()
insertPrice = "INSERT INTO public.prices (item_id, day, price) VALUES (%s, %s, %s)"
insertVolume = "INSERT INTO public.volume (item_id, day, volume) VALUES (%s, %s, %s)"
                
for i, name in enumerate(names):
    localHistory = {}
    localVolume = {}
    url = base + names_formatted[i] + extension
    print(name)
    try:
        response = requests.get(url)
    except:
        webErrors.append(name)
    else:
        soup = BeautifulSoup(response.content, 'html5lib')
        prices = [x.getText() for x in soup.find_all("span", {"class", "s1"})]
        for price in prices:
            temp = price.replace("'", "").split(":")
            params = (items[i][0], int(temp[0]), int(temp[1]))
            db.insert(insertPrice, params)
            if(len(temp) == 3):
                params = (items[i][0], int(temp[0]), int(temp[2]))
                db.insert(insertVolume, params)



