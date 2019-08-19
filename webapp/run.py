import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


def get_price(m, scaler, flat_type, flat_size, flat_locality):
    flat_data = scaler.transform(pd.DataFrame([[flat_type, flat_size, flat_locality]]))
    return m.predict(flat_data)


model = joblib.load('./models/price-predictor.joblib')

info = pd.read_csv('./data/flats_info.csv')
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

application = Flask(__name__, template_folder='./frontend/dist/', static_folder='./frontend/dist/static')
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'


@application.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predict():
    data = request.get_json(force=True)
    print(data)
    prediction = get_price(model, scaler_X, data.get('type', False), data.get('size', False),
                           data.get('locality', False))
    response = jsonify((scaler_Y.inverse_transform(prediction))[0])
    return response


@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
