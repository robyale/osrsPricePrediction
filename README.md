# osrsPricePrediction
## Installation and Use
To install the required dependencies, use the following command
```
pip install -r requirements.txt
```

To set up the database, follow the [PostgreSQL Getting Started documentation](https://www.postgresql.org/docs/12/tutorial-start.html)

Then, open up pgAdmin and connect it to your database. Using the query tool under tools, upload the schema.sql file to set up the database. Be sure to update database_connect.py with the necessary database information in order to connect to the database.

Run main.py, and a plot with the training data, actual data, and predicted data will show. You can change the item id where the variable prices are declared. 

## Background
The first video game I ever played is the MMORPG RuneScape around 2007. I've moved on from the game, but the developers brought back a version of RuneScape called Old School RuneScape (OSRS) based on the build in 2007. Inside the game there is a stock market like place called the Grand Exchange (GE) where players can buy and sell items. With over 80,000 players at any given moment and thousands of real-world dollars being circulated in this game, there is an opportunity for profit (Some people even sell online currency for a living!). There are no transaction fees, and not much financial analysis of Grand Exchange. I decided it would be a good project to learn about data scraping, financial models, and machine learning among other coding skills. I don't expect to make any profit, but it's a neat concept to think about!
## This Project
My goal for this project is to 1) learn the basics of machine learning to predict price, 2) learn financial analysis to determine the right items to trade, and 3) apply my knowledge of data science to process the large amount of data in the OSRS API. I will be using Python throughout the project, with a PostgreSQL database to handle the large amount of data.
## Getting OSRS Data
So far, I can retrieve item names and ids from an API called [osrsbox](https://www.osrsbox.com/projects/osrsbox-db/). The API returns a .json file, which is parsed, checked to see if the item is tradable, and stored in a PostgreSQL database. The game is updated weekly, so every Monday the program checks and updates the item list. To retrieve the price information, I originally used the official OSRS API. However, they would limit multiple responses, which greatly slowed down data retrival. I luckily stumbled upon the (private) data pages that OSRS utilized to make their price graphs. Using data scraping, I was able to take this webpage, parse the data, and insert the entirety of the price and volume data of the GE. This sped up data retrieval from days to 3 hours for initializing the database, and allowed for retrieval of the entirety of price data instead of getting the past 180 days.
## Building the machine learning model
I will be using LSTM model to build and train a basic machine learning model. The model will only use past price history, so I don't expect it to be accurate. I have a basic model set up, but since I only have 180 days of price data the predictions vary wildly. I hope to expand on this model in future versions
## Problems
While I sped up the data retrieval from days to 3 hours, the data retrieval is still slow. It will take about the same amount of time to update the database vs initializing the database with the entirety of price information. 

There are also considerable trading limits on the volume of items I can sell. First, all trades have to be done by hand (I could use a bot, but that could lead to an IP address ban). Each account can only sell 8 items at a given time. A 25,000 trade limit is in place for free-to-play players, and there are more limits on specific items.

Building and training the model takes considerable time for each item set. Each item takes about 40 seconds, so for the entire 3,700 item database it will take about 41 hours of continuous running. I will need a way to filter out items that will most likely not make money.
## Upcoming iterations
The program needs to be expanded to accommodate the extra items. At the moment, I am working with only 5 items due to the slow nature of getting price data and building/training the machine learning model. For the next iteration, I will be working on using multithreading to speed up the process. I just implemented my machine learning model, so I would like to expand more on using the model to predict pricing. I hope to filter the items so that I only have high-volume, medium-priced items. Using these two factors I should be able to cut down on items I can trade considerably. Lastly, I hope to use some sort of financial models to supplement the machine learning model. This is still in the very early stages of development, so I hope to expand what I have greatly.
