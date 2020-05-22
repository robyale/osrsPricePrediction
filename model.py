#!python
# -*- coding: utf-8 -*-

""" Builds, trains, and tests LSTM model
    for predicting Old School Runescrape 
    GE prices. Plots and gives some stats
    on how well the model did.
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

__author__ = "Rob Yale"
__version__ = "1.0.0"
__status__ = "Prototype"

class model(object):
    # Scales data between 0 and 1
    def scaleData(self):
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(self.data)
        return scaled_data, scaler

    # Create and shapes training data
    def shapeData(self):
        # Scale the data
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(self.data)

        # Set up scaled training data
        train_data = self.scaled_data[0:self.training_data_len, :]

        # Split data into x_train and y_train datasets
        x_train = []
        y_train = []
        for i in range(self.numDays, len(train_data)):
            x_train.append(train_data[i-self.numDays:i, 0])
            y_train.append(train_data[i, 0])

        # Convert x_train and y_train into numpy arrays
        x_train, y_train = np.array(x_train), np.array(y_train)

        # Reshape the data
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        return x_train, y_train

    # Builds and trains the LSTM model
    def trainModel(self):
        # Set up training data
        x_train, y_train = self.shapeData()

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        # Compile the model
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size=1, epochs=1)

        return model

    # Gets prediction and rmse of model
    def predictModel(self):
        model = self.trainModel()
        training_data_len = self.training_data_len
        scaled_data = self.scaled_data
        numDays = self.numDays

        # Create the testing data set
        # Create new array with scaled data
        test_data = scaled_data[training_data_len - numDays:, :]

        # Create x_test and y_test datasets
        x_test = []
        dataSet = np.array(self.data)
        y_test = dataSet[training_data_len:, :]
        for i in range(numDays, len(test_data)):
            x_test.append(test_data[i-numDays:i, 0])

        # Convert to numpy array and reshape the data
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # Get the predicted price values
        predictions = model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - y_test)**2)

        return predictions, rmse

    # Plots the actual and predicted data
    def plotData(self, predictions=None):
        # Get training data
        train = self.data[:self.training_data_len]
        if(predictions == None):
            predictions, rmse = self.predictModel()

        # Get actual values
        valid = {}
        temp = [val for sublist in self.data for val in sublist]
        for i in range(self.training_data_len - 1, len(self.data)):
            valid[i] = temp[i]

        # Predicted values
        temp = [val for sublist in predictions for val in sublist]
        predictions = {}
        for i in range(self.training_data_len, len(self.data)):
            predictions[i] = temp[i-self.training_data_len]

        # Plot
        plt.figure(figsize=(16, 8))
        plt.title('Model')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Price in coins', fontsize=18)
        plt.plot(train)
        plt.plot(*zip(*sorted(valid.items())))
        plt.plot(*zip(*sorted(predictions.items())))
        plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
        plt.show()


    def __init__(self, data, numDays = 30):
        self.data = data
        self.training_data_len = len(data) - 10
        self.numDays = numDays
        self.scaled_data, self.scaler = self.scaleData()
