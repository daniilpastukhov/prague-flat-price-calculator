import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.svm import SVR
from joblib import dump

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


def get_price(m, scaler, flat_type, flat_size, flat_locality):
    flat_data = scaler_X.transform(np.array([[flat_types[flat_type], flat_size, regions[flat_locality]]]))
    return m.predict(flat_data)


info = pd.read_csv('../data/flats_info.csv')
info = info.drop('id', 1)
col_names = list(info.columns)
info = info.dropna()

p = info['price'] < 100000
info = info[p]  # Get information only about flats with price < 100'000
m = len(info)  # Number of examples

X = info[['type', 'size', 'locality']].values
y = info['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

scaler_X = preprocessing.StandardScaler().fit(X_train)
scaler_Y = preprocessing.StandardScaler().fit(y_train.reshape(-1, 1))
X_train = scaler_X.transform(X_train)
y_train = scaler_Y.transform(y_train.reshape(-1, 1))
y_train = y_train.reshape(-1)
X_test = scaler_X.transform(X_test)
y_test = scaler_Y.transform(y_test.reshape(-1, 1))
y_test = y_test.reshape(-1)

model = SVR(kernel='rbf', epsilon=0.01, gamma='auto')
model.fit(X_train, y_train)

scores = cross_val_score(model, X_test, y_test, cv=3)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

dump(model, 'price-predictor.joblib')

# print(scaler_Y.inverse_transform(get_price(model, scaler_X, '2+kt', 59, 'Praha 2')))
# print(scaler_Y.inverse_transform(get_price(model, scaler_X, 'unusual', 160, 'Praha 9')))
# print(scaler_Y.inverse_transform(get_price(model, scaler_X, '1+kt', 25, 'Praha 1')))
# print(scaler_Y.inverse_transform(get_price(model, scaler_X, '3+1', 87, 'Praha 5')))
# print(scaler_Y.inverse_transform(get_price(model, scaler_X, 'flatshare', 23, 'Praha 6')))
