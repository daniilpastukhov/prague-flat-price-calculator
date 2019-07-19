import pandas as pd
import numpy as np
import pickle

from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

flat_types = {
    'flatshare': 11,
    '1+kt': 1,
    '1+1': 2,
    '2+kt': 3,
    '2+1': 4,
    '3+kt': 5,
    '3+1': 6,
    '4+kt': 7,
    '4+1': 8,
    '5+kt': 9,
    '5+1': 10,
    'unusual': 12,
    'Unknown': None
}

regions = {
    'Praha': 0,
    'Praha 1': 1,
    'Praha 2': 2,
    'Praha 3': 3,
    'Praha 4': 4,
    'Praha 5': 5,
    'Praha 6': 6,
    'Praha 7': 7,
    'Praha 8': 8,
    'Praha 9': 9,
    'Praha 10': 10,
    'Praha 11': 11
}

info = pd.read_csv('flats_info.csv')
info = info.drop('id', 1)
col_names = list(info.columns)
info = info.fillna(info.mean())  # Fill NaN's with column's mean value

p = info['price'] < 100000
info = info[p]  # Get information only about flats with price < 100'000
info['price'] = info['price'].round(decimals=3)  # Round prices to 3 decimals places
m = len(info)  # Number of examples

X = info[['type', 'size', 'locality']].values
y = info['price'].values

scaler_X = StandardScaler().fit(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scalerX = StandardScaler().fit(X_train)
scalery = StandardScaler().fit(y_train)
X_train = scalerX.transform(X_train)
y_train = scalery.transform(y_train)
X_test = scalerX.transform(X_test)
y_test = scalery.transform(y_test)

model = linear_model.SGDRegressor(max_iter=1000, tol=1e-3, eta0=0.0001, random_state=42)
model.fit(X_train, y_train)

scores = cross_val_score(model, X_test, y_test, cv=3)

# print(info.describe())

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

data_to_predict = pd.DataFrame([[2, 80, 6]])
data_to_predict2 = scaler_X.transform(data_to_predict)

print(data_to_predict2)

print(model.predict(data_to_predict2))

# print(round(get_price('2+kt', 59, 'Praha 2')))
# print(round(get_price('unusual', 160, 'Praha 9')))
# print(round(get_price('1+kt', 25, 'Praha 1')))
# print(round(get_price('3+1', 87, 'Praha 5')))
# print(round(get_price('flatshare', 23, 'Praha 6')))
