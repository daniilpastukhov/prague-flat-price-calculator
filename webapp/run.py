import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

models_path = './models/'
data_path = './data/'
scaler_path = './models/scalers/'

cities = ['prague', 'brno']


def load_scalers():
    scalers_list = {}
    for city in cities:
        scalers_list[city] = joblib.load(scaler_path + 'scalerx-' + city + '.joblib')
    return scalers_list


def get_price(m, scaler, flat_type, flat_size, flat_locality):
    flat_data = scaler.transform(pd.DataFrame([[flat_type, flat_size, flat_locality]]))
    return m.predict(flat_data)[0]


models = {'prague': joblib.load('./models/price-predictor-prague.joblib'),
          'brno': joblib.load('./models/price-predictor-brno.joblib')}

scalers = load_scalers()

application = Flask(__name__, template_folder='./frontend/dist/', static_folder='./frontend/dist/static')
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

print(scalers['brno'])
print(models['brno'])

@application.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predict():
    data = request.get_json(force=True)
    request_city = data.get('city', False)
    prediction = get_price(models[request_city], scalers[request_city], data.get('type', False),
                           data.get('size', False), data.get('locality', False))
    return jsonify(prediction)


@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
