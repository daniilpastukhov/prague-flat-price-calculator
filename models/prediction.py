import pandas as pd
import numpy as np
import pickle

from sklearn import ensemble
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.svm import SVR
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

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

info = pd.read_csv('../data/flats_info.csv')
info = info.drop('id', 1)
col_names = list(info.columns)
info = info.dropna()

p = info['price'] < 100000
info = info[p]  # Get information only about flats with price < 100'000
m = len(info)  # Number of examples

scaler = preprocessing.StandardScaler().fit(info)
info = scaler.transform(info)
info = pd.DataFrame(info, columns=col_names)

X = info[['type', 'size', 'locality']].values
y = info['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

rs = 1
ests = [linear_model.LinearRegression(), linear_model.Ridge(),
        linear_model.Lasso(), linear_model.ElasticNet(),
        linear_model.BayesianRidge(), linear_model.OrthogonalMatchingPursuit(),
        linear_model.SGDRegressor(), SVR(kernel='rbf')]

ests_labels = np.array(['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'BayesRidge', 'OMP', 'SGD', 'SVR'])
errvals = np.array([])

for e in ests:
    e.fit(X_train, y_train)
    this_err = metrics.median_absolute_error(y_test, e.predict(X_test))
    print("got error %0.2f" % this_err)
    errvals = np.append(errvals, this_err)

pos = np.arange(errvals.shape[0])
srt = np.argsort(errvals)
plt.figure(figsize=(7, 5))
plt.bar(pos, errvals[srt], align='center')
plt.xticks(pos, ests_labels[srt])
plt.xlabel('Estimator')
plt.ylabel('Median Absolute Error')
plt.show()

model = SVR()
model.fit(X_train, y_train)

scores = cross_val_score(model, X_test, y_test, cv=3)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# data_to_predict = scaler.inverse_transform(np.array([2, 80, 6]))
# print(model.predict(data_to_predict))

# print(round(get_price('2+kt', 59, 'Praha 2')))
# print(round(get_price('unusual', 160, 'Praha 9')))
# print(round(get_price('1+kt', 25, 'Praha 1')))
# print(round(get_price('3+1', 87, 'Praha 5')))
# print(round(get_price('flatshare', 23, 'Praha 6')))
