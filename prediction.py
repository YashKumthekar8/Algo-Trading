import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional
from sklearn.preprocessing import MinMaxScaler

# endDate = datetime.now()
# startDate = datetime(endDate.year-1, endDate.month, endDate.day)
# data = get_history('INFY', startDate, endDate)
# print(data.tail(10))


companies_symbols = ['INFY', 'TCS', 'M&M', 'RELIANCE']

def fetch_data(companies):
    df = pd.DataFrame()
    for i in range(0, len(companies)):
        endDate = datetime.now()
        startDate = datetime(endDate.year-5, endDate.month, endDate.day)
        data_ = get_history(companies[i], startDate, endDate)
        df = pd.concat([df, data_], axis=0)

    return df


def fetch_data_company_wise(company_name):
    endDate = datetime.now()
    startDate = datetime(endDate.year-1, endDate.month, endDate.day)
    data = get_history(company_name, startDate, endDate)
    return data


def preprocess_data(dataset):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    return scaled_data, scaler


def data_preparation(scaled_data, time_step, future_days):
    # Multi step data preparation

    # split into samples
    X_samples = list()
    y_samples = list()

    NumerOfRows = len(scaled_data)
    TimeSteps=time_step  # next few day's Price Prediction is based on last how many past day's prices
    FutureTimeSteps=future_days # How many days in future you want to predict the prices

    # Iterate thru the values to create combinations
    for i in range(TimeSteps , NumerOfRows-FutureTimeSteps , 1):
        x_sample = scaled_data[i-TimeSteps:i]
        y_sample = scaled_data[i:i+FutureTimeSteps]
        X_samples.append(x_sample)
        y_samples.append(y_sample)

    ################################################

    # Reshape the Input as a 3D (samples, Time Steps, Features)
    X_data=np.array(X_samples)
    X_data=X_data.reshape(X_data.shape[0],X_data.shape[1], 1)
    print('### Input Data Shape ###')
    print(X_data.shape)

    # We do not reshape y as a 3D data  as it is supposed to be a single column only
    y_data=np.array(y_samples)
    print('### Output Data Shape ###')
    print(y_data.shape)
    return X_data, y_data


def data_split(X_data, y_data, testing_rec):
    # Choosing the number of testing data records
    TestingRecords=testing_rec

    # Splitting the data into train and test
    X_train=X_data[:-TestingRecords]
    X_test=X_data[-TestingRecords:]
    y_train=y_data[:-TestingRecords]
    y_test=y_data[-TestingRecords:]

    ############################################

    # Printing the shape of training and testing
    print('\n#### Training Data shape ####')
    print(X_train.shape)
    print(y_train.shape)
    print('\n#### Testing Data shape ####')
    print(X_test.shape)
    print(y_test.shape)

    return X_train, y_train, X_test, y_test


def decide_timesteps(X_train):
    TimeSteps = X_train.shape[1]
    total_features = X_train.shape[2]
    return TimeSteps


def model(X_train, y_train, X_test, y_test, df, TimeSteps, FutureTimeSteps, scaler):

    model = Sequential([
        Bidirectional(LSTM(128, return_sequences=True)),
        Bidirectional(LSTM(64, return_sequences=True)),
        Bidirectional(LSTM(64, return_sequences=True)),
        Bidirectional(LSTM(32, return_sequences=True)),
        Bidirectional(LSTM(32, return_sequences=False)),
        Dense(TimeSteps),
        Dense(FutureTimeSteps)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    import time
    startTime = time.time()
    history = model.fit(X_train, y_train, batch_size=5, epochs=100)
    endTime = time.time()
    print(f'Time taken : {(endTime - startTime) / 60} minutes')


    # Making predictions on test data
    predicted_Price = model.predict(X_test)
    predicted_Price = scaler.inverse_transform(predicted_Price)
    print('#### Predicted Prices ####')
    # print(predicted_Price)


    # Making predictions on test data
    LastxDays = np.array(df.tail(TimeSteps)['Close'])
    LastxDays = scaler.fit_transform(LastxDays.reshape(-1, 1))

    X_test = scaler.transform(LastxDays)

    NumSamples = 1
    TimeStep = X_test.shape[0]
    NumFeatures = X_test.shape[1]
    X_test = X_test.reshape(NumSamples, TimeStep, NumFeatures)
    # Generating the predictions for next 5 days
    NextxDaysPrice = model.predict(X_test)

    # Generating the prices in original scale
    NextxDaysPrice = scaler.inverse_transform(NextxDaysPrice)
    return NextxDaysPrice, predicted_Price


def decide_steps(future_days):
    if future_days == 5:
        time_step = 25
        testing_rec = 10
    elif future_days == 10:
        time_step = 50
        testing_rec = 20
    else:
        time_step = 75
        testing_rec = 30
    return time_step, testing_rec


future_days = 10  # Take it from the user
time_step, testing_rec = decide_steps(future_days)
df = fetch_data_company_wise('RELIANCE')
data = df.filter(['Close'])
dataset = data.values
scaled_data, scaler = preprocess_data(dataset)
x_data, y_data = data_preparation(scaled_data, time_step, future_days)
X_train, y_train, X_test, y_test = data_split(x_data, y_data, testing_rec)
TimeSteps = decide_timesteps(X_train)
NextxDaysPrice, predicted_Price = model(X_train, y_train, X_test, y_test, 
                    df, time_step, future_days, scaler)
print(NextxDaysPrice)



# Future days =    5, 10, 15
# TimeSteps =      25, 50, 75
# TestingRecords = 10, 20, 30

