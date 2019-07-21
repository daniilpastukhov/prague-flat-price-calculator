import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.svm import SVR
import sklearn.metrics as metrics
import matplotlib.pyplot as plt

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

estimators = [linear_model.LinearRegression(), linear_model.Ridge(),
              linear_model.Lasso(), linear_model.ElasticNet(),
              linear_model.BayesianRidge(), linear_model.OrthogonalMatchingPursuit(),
              linear_model.SGDRegressor(), SVR(kernel='rbf')]

estimator_labels = np.array(['Linear', 'Ridge', 'Lasso', 'ElasticNet', 'BayesRidge', 'OMP', 'SGD', 'SVR'])
estimator_values = np.array([])

for e in estimators:
    e.fit(X_train, y_train)
    this_err = metrics.median_absolute_error(y_test, e.predict(X_test))
    print("Got error %0.2f" % this_err)
    estimator_values = np.append(estimator_values, this_err)

pos = np.arange(estimator_values.shape[0])
srt = np.argsort(estimator_values)
plt.figure(figsize=(7, 5))
plt.bar(pos, estimator_values[srt], align='center')
plt.xticks(pos, estimator_labels[srt])
plt.xlabel('Estimator')
plt.ylabel('Median Absolute Error')
plt.show()
