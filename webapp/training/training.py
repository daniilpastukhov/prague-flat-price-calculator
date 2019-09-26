import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from joblib import dump
import os
import catboost


def make_model(path, model_name, region):
    info = pd.read_csv(path)
    info = info.dropna(axis=0)

    f = info['price'] < 100000
    info = info[f]  # Get information only about flats with price < 100'000

    X = info[['type', 'size', 'locality']].values
    y = info['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

    scaler_X = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler_X.transform(X_train)
    X_test = scaler_X.transform(X_test)

    # model = catboost.CatBoostRegressor(verbose=False)
    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("MSE train: ", np.sqrt(mean_squared_error(y_train, model.predict(X_train))))
    print("MSE: ", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("-" * 100)

    # scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    # print("MSE: %0.2f" % (np.sqrt(-scores.mean())))

    dump(model, model_name + '.joblib', protocol=2)  # Save model
    dump(scaler_X, 'scalerx-' + region + '.joblib', protocol=2)
    os.rename('./scalerx-' + region + '.joblib', './scalers/scalerx-' + region + '.joblib')


make_model('../data/flats_prague_numeric.csv', 'price-predictor-prague', 'prague')
make_model('../data/flats_brno_numeric.csv', 'price-predictor-brno', 'brno')
