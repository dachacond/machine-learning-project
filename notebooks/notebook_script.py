# Standard Library Imports
import math
import json
import logging

# General Imports
import pandas as pd

# SKLearn Imports

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report, RocCurveDisplay

# Load Data
df = pd.read_csv('../data/train.csv')
df.info()

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 6973 entries, 0 to 6972
# Data columns (total 8 columns):
#  #   Column  Non-Null Count  Dtype  
# ---  ------  --------------  -----  
#  0   y       6973 non-null   int64  
#  1   x1      6973 non-null   float64
#  2   x2      6973 non-null   float64
#  3   x3      6973 non-null   object 
#  4   x4      6545 non-null   float64
#  5   x5      6097 non-null   float64
#  6   x6      5738 non-null   object 
#  7   x7      5401 non-null   object 
# dtypes: float64(4), int64(1), object(3)
# memory usage: 435.9+ KB

df.head(5)

# 	y	x1	x2	x3	x4	x5	x6	x7
# 0	0	4.119524	22.681276	Tue	-2.367208	104.295597	Oregon	mercedes
# 1	0	-0.595945	22.106476	Wed	0.357183	72.786564	Minnesota	subaru
# 2	0	5.078628	22.297878	Tue	-2.328044	106.196520	Virginia	toyota
# 3	0	3.543362	20.281846	Wed	1.323722	107.424498	North Dakota	chevrolet
# 4	0	1.462608	19.958180	Thu	2.525927	112.433096	Georgia	chevrolet

df.x6.unique()

# array(['Oregon', 'Minnesota', 'Virginia', 'North Dakota', 'Georgia',
#        'Delaware', 'California', nan, 'Colorado', 'Florida', 'Wisconsin',
#        'North Carolina', 'Massachusetts', 'Louisiana', 'New Mexico',
#        'New Jersey', 'Texas', 'Indiana', 'Maine', 'Alabama', 'Oklahoma',
#        'Kentucky', 'New York', 'New Hampshire', 'Ohio', 'Nevada', 'Idaho',
#        'Illinois', 'West Virginia', 'Tennessee', 'Arizona', 'Kansas',
#        'Vermont', 'Wyoming', 'South Carolina', 'Maryland', 'Michigan',
#        'Connecticut', 'Rhode Island', 'DC', 'Mississippi', 'Hawaii',
#        'Pennsylvania', 'Washington', 'Utah', 'Montana', 'Missouri',
#        'Nebraska', 'Iowa', 'Alaska', 'South Dakota', 'Arkansas'],
#       dtype=object)

df.x7.unique()

# array(['mercedes', 'subaru', 'toyota', 'chevrolet', 'ford', nan, 'nissan',
#        'buick'], dtype=object)

df_X = df.drop("y", axis=1)
df_label = df["y"]

df_X.head()

# x1	x2	x3	x4	x5	x6	x7
# 0	4.119524	22.681276	Tue	-2.367208	104.295597	Oregon	mercedes
# 1	-0.595945	22.106476	Wed	0.357183	72.786564	Minnesota	subaru
# 2	5.078628	22.297878	Tue	-2.328044	106.196520	Virginia	toyota
# 3	3.543362	20.281846	Wed	1.323722	107.424498	North Dakota	chevrolet
# 4	1.462608	19.958180	Thu	2.525927	112.433096	Georgia	chevrolet

numeric_features = ["x1", "x2", "x4", "x5"]
numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
)

categorical_features = ["x3", "x6", "x7"]
categorical_transformer = OneHotEncoder(handle_unknown="infrequent_if_exist")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

clf = Pipeline(
    steps=[("preprocessor", preprocessor),
           ("classifier", LogisticRegression(max_iter=10000))]
)

clf

# Pipeline
# Pipeline(steps=[('preprocessor',
#                  ColumnTransformer(transformers=[('num',
#                                                   Pipeline(steps=[('imputer',
#                                                                    SimpleImputer(strategy='median')),
#                                                                   ('scaler',
#                                                                    StandardScaler())]),
#                                                   ['x1', 'x2', 'x4', 'x5']),
#                                                  ('cat',
#                                                   OneHotEncoder(handle_unknown='infrequent_if_exist'),
#                                                   ['x3', 'x6', 'x7'])])),
#                 ('classifier', LogisticRegression(max_iter=10000))])
# preprocessor: ColumnTransformer
# ColumnTransformer(transformers=[('num',
#                                  Pipeline(steps=[('imputer',
#                                                   SimpleImputer(strategy='median')),
#                                                  ('scaler', StandardScaler())]),
#                                  ['x1', 'x2', 'x4', 'x5']),
#                                 ('cat',
#                                  OneHotEncoder(handle_unknown='infrequent_if_exist'),
#                                  ['x3', 'x6', 'x7'])])
# num
# ['x1', 'x2', 'x4', 'x5']

# SimpleImputer
# SimpleImputer(strategy='median')

# StandardScaler
# StandardScaler()
# cat
# ['x3', 'x6', 'x7']

# OneHotEncoder
# OneHotEncoder(handle_unknown='infrequent_if_exist')

# LogisticRegression
# LogisticRegression(max_iter=10000)

# Make LogReg Pipeline

RANDOM_STATE=1337

X_train, X_test, y_train, y_test = train_test_split(
    df_X,
    df_label,
    random_state=RANDOM_STATE
    )

clf.fit(X_train, y_train)

# Pipeline
# Pipeline(steps=[('preprocessor',
#                  ColumnTransformer(transformers=[('num',
#                                                   Pipeline(steps=[('imputer',
#                                                                    SimpleImputer(strategy='median')),
#                                                                   ('scaler',
#                                                                    StandardScaler())]),
#                                                   ['x1', 'x2', 'x4', 'x5']),
#                                                  ('cat',
#                                                   OneHotEncoder(handle_unknown='infrequent_if_exist'),
#                                                   ['x3', 'x6', 'x7'])])),
#                 ('classifier', LogisticRegression(max_iter=10000))])
# preprocessor: ColumnTransformer
# ColumnTransformer(transformers=[('num',
#                                  Pipeline(steps=[('imputer',
#                                                   SimpleImputer(strategy='median')),
#                                                  ('scaler', StandardScaler())]),
#                                  ['x1', 'x2', 'x4', 'x5']),
#                                 ('cat',
#                                  OneHotEncoder(handle_unknown='infrequent_if_exist'),
#                                  ['x3', 'x6', 'x7'])])
# num
# ['x1', 'x2', 'x4', 'x5']

# SimpleImputer
# SimpleImputer(strategy='median')

# StandardScaler
# StandardScaler()
# cat
# ['x3', 'x6', 'x7']

# OneHotEncoder
# OneHotEncoder(handle_unknown='infrequent_if_exist')

# LogisticRegression
# LogisticRegression(max_iter=10000)

print("model score: %.3f" % clf.score(X_test, y_test))

# model score: 0.556

tprobs = clf.predict_proba(X_test)[:, 1]
print(classification_report(y_test, clf.predict(X_test)))
print('Confusion matrix:')
print(confusion_matrix(y_test, clf.predict(X_test)))
print(f'AUC: {roc_auc_score(y_test, tprobs)}')
RocCurveDisplay.from_estimator(estimator=clf,X= X_test, y=y_test)

#  precision    recall  f1-score   support

#            0       0.54      0.60      0.57       848
#            1       0.58      0.52      0.54       896

#     accuracy                           0.56      1744
#    macro avg       0.56      0.56      0.56      1744
# weighted avg       0.56      0.56      0.56      1744

# Confusion matrix:
# [[508 340]
#  [434 462]]
# AUC: 0.5875352720687332