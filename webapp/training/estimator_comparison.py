import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

prague_path = '../data/flats_prague_numeric.csv'
brno_path = '../data/flats_brno_numeric.csv'


def get_stats(path):
    info = pd.read_csv(path)
    info = info.dropna()

    f = info['price'] < 100000
    info = info[f]  # Get information only about flats with price < 100'000

    X = info[['type', 'size', 'locality']].values
    scaler_X = preprocessing.StandardScaler().fit(X)
    X = scaler_X.transform(X)
    y = info['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

    estimators = [linear_model.LinearRegression(), linear_model.Ridge(alpha=0.1),
                  linear_model.Lasso(alpha=0.1), linear_model.ElasticNet(alpha=0.01, l1_ratio=0.25),
                  linear_model.BayesianRidge(n_iter=500), linear_model.OrthogonalMatchingPursuit(),
                  linear_model.SGDRegressor(max_iter=2500, epsilon=0.01), SVR(kernel='rbf', epsilon=0.01, C=20)]

    estimator_values = np.array([])

    for e in estimators:
        e.fit(X_train, y_train)
        this_err = metrics.median_absolute_error(y_test, e.predict(X_test))
        estimator_values = np.append(estimator_values, this_err)

    return estimator_values


def find_best(path, model, params):
    info = pd.read_csv(path)
    info = info.dropna()

    f = info['price'] < 100000
    info = info[f]  # Get information only about flats with price < 100'000

    X = info[['type', 'size', 'locality']].values
    scaler_X = preprocessing.StandardScaler().fit(X)
    X = scaler_X.transform(X)
    y = info['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

    cv = GridSearchCV(model, params, scoring='neg_mean_squared_error', cv=5)
    cv.fit(X_train, y_train)
    print(cv.best_params_)

    cv_results = cv.cv_results_
    for mean_score, parameters in zip(cv_results['mean_test_score'], cv_results['params']):
        print(np.sqrt(-mean_score), parameters)


estimator_labels = np.array(['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'BayesRidge', 'OMP', 'SGD', 'SVR'])
estimator_values_prague = get_stats(prague_path)
estimator_values_brno = get_stats(brno_path)


pos = np.arange(estimator_values_prague.shape[0])
srt = np.argsort(estimator_values_prague)
plt.figure(figsize=(7, 5))
p1 = plt.bar(pos, estimator_values_prague[srt], align='center', color='blue')
p2 = plt.bar(pos, estimator_values_brno[srt], align='center', color='red')
plt.xticks(pos, estimator_labels[srt])
plt.title('Estimators comparison')
plt.xlabel('Estimator')
plt.ylabel('Median Absolute Error')
plt.show()

params = [
    {'n_estimators': [50, 100, 150, 200], 'max_depth': [6, 8, 10, 12, 14]},
    {'bootstrap': [False], 'n_estimators': [50, 100, 150, 200], 'max_depth': [6, 8, 10, 12, 14]}
]

find_best(prague_path, RandomForestRegressor(random_state=42), params)
