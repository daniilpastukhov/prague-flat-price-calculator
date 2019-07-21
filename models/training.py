import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.svm import SVR
from joblib import dump

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

dump(model, 'price-predictor.joblib')  # Save model
