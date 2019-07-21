import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

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
    flat_data = scaler.transform(np.array([[flat_types[flat_type], flat_size, regions[flat_locality]]]))
    return m.predict(flat_data)


model = joblib.load('../../models/price-predictor.joblib')

info = pd.read_csv('../../data/flats_info.csv')
info = info.drop('id', 1)
info = info.dropna()

p = info['price'] < 100000
info = info[p]  # Get information only about flats with price < 100'000
m = len(info)  # Number of examples

X = info[['type', 'size', 'locality']].values
y = info['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

scaler_X = preprocessing.StandardScaler().fit(X_train)
scaler_Y = preprocessing.StandardScaler().fit(y_train.reshape(-1, 1))

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = get_price(model, scaler_X, data['type'], data['size'], data['locality'])
    return jsonify(prediction)


if __name__ == '__main__':
    app.run(port=8080)
