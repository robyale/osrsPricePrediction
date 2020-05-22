# osrsPricePrediction
## Installation and Use
To install the required dependancies, use the following command
```
pip install -r requirements.txt
```

To set up the database, follow the [PostgreSQL Getting Started documentation](https://www.postgresql.org/docs/12/tutorial-start.html)

Then, use the schema in schema.sql to set up the database. The code (at the moment) will not work without some price data in the data. It is necessary to go to the [Old School Runescape price API for cannonballs](http://services.runescape.com/m=itemdb_oldschool/api/graph/2.json), and get the earliest date (which should be the first date value in milliseconds since epoch). You can easily insert this into your database with pgAdmin, or use a command line insert statement. Be sure to update database_connect.py with the necessary database information in order to connect.

Run main.py, and a plot with the training data, actual data, and predicted data will show. You can change the item id where the variable prices is declared. 

## Background
The first video game I ever played is the MMORPG Runescape around 2007. I've moved on from the game, but the developers brought back a version of Runescape called Old School Runescape (OSRS) based on the build in 2007. Inside the game there is a stock market like place called the Grand Exchange where players can buy and sell items. With over 80,000 players at any given moment and thousands of real world dollars being circulated in this game, there is an opportunity for profit (Some people even sell online currency for a living!). There are no transaction fees, and not much financial analysis of Grand Exchange. I decided it would be a good project to learn about data scraping, financial models, and machine learning among other coding skills. I don't expect to make any profit, but it's a neat concept to think about!
## This Project
My goal for this project is to 1) learn the basics of machine learning to predict price, 2) learn financial analysis to determine the right items to trade, and 3) apply my knowledge of datascience to process the large amount of data in the OSRS API. I will be using Python throughout the project, with a PostgreSQL database to handle the large amount of data.
## Getting OSRS Data
So far, I can retrieve item names and ids from an API called [osrsbox](https://www.osrsbox.com/projects/osrsbox-db/). The API returns a .json file, which is parsed, checked to see if the item is tradable, and stored in a PostgreSQL database. The game is updated weekly, so every monday the program checks and updates the item list. To retrieve the price information, the developers of OSRS made a json API that outputs the average price of items for the past 180 days. I get the json file for a particular item id, and then I update the price data for that item in the PostgreSQL database. I will be expanding this to include other financial information to make decisions on what items to trade.
## Building the machine learning model
I will be using LSTM model to build and train a basic machine learning model. The model will only use past price history, so I don't expect it to be accurate. I have a basic model set up, but since I only have 180 days of price data the predictions vary wildly. I hope to expand on this model in future versions
## Problems
The OSRS API for getting price information will refuse connection after repeated attempts to access their API. Thus, I have to rely on certain delays to ensure I am getting data for items. I can only get price information for one item at a time, so even updating pricing for 1 day takes a long time. Even at a 3 second delay per item, it takes over 3 hours to update all the necessary information. 

The maximum amount of price data I could find went back only 180 days. Since there is such little data, the machine learning model is going to off considerably. The only way to get more data is to wait, so it will take time to build up a considerable database of price information. 

There is also considerable trading limits on the volume of items I can sell. First, all trades have to be done by hand (I could use a bot, but that could lead to an IP address ban). Each account can only sell 8 items at a given time. A 25,000 trade limit is in place for free-to-play players.
## Future Versions
In future versions, I will be updating the database_connect.py to initialize the database if there is no data in the database. The program needs to be expanded to accomodate the extra items. At the moment, I am working with only 5 items due to the slow nature of getting price data and building/training the machine learning model. I just implemented my machine learning model, so I would like to expand more on using the model to predict pricing. I hope to filter the items so that I only have high-volume, medium-priced items. Using these two factors I should be able to cut down on items I can trade considerably. Lastly, I hope to use some sort of financial models to supplement the machine learning model. This is still in the very early stages of development, so I hope to expand what I have greatly.
