import base64

import pandas as pd
import matplotlib.pyplot as plt
from seaborn.external.six import StringIO
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, r2_score
import pickle, os, joblib
import seaborn as sb
import numpy as np

data_set = pd.read_csv(r'C:\Users\newac\Desktop\C964-Update\stroke_data.csv')
# Remove ID Column
data_set.drop('id', axis=1, inplace=True)
# Fill missing BMI values
data_set['bmi'].fillna(data_set['bmi'].mean(), inplace=True)

# Create label encoder to transform the object data types to int for model to use
encode = LabelEncoder()
# Gender
gender = encode.fit_transform(data_set['gender'])
data_set['gender'] = gender
# Marriage Status
married = encode.fit_transform(data_set['ever_married'])
data_set['ever_married'] = married
# Work Type
work = encode.fit_transform(data_set['work_type'])
data_set['work_type'] = work
# Residence Type
residence = encode.fit_transform(data_set['Residence_type'])
data_set['Residence_type'] = residence
# Smoking Status
smoke = encode.fit_transform(data_set['smoking_status'])
data_set['smoking_status'] = smoke

# Prepare & Train
x = data_set.drop('stroke', axis=1)
y = data_set['stroke']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=None)

# Scale down the data
scaler = StandardScaler()
x_train_scale = scaler.fit_transform(x_train)
x_test_scale = scaler.transform(x_test)

# Logistical Regression
log_reg = LogisticRegression()
log_reg.fit(x_train_scale, y_train)
y_pred = log_reg.predict(x_test_scale)


def make_prediction(input):
    x = scaler.transform(input)
    return log_reg.predict(x)


def display_probability(input):
    x = scaler.transform(input)
    return round(log_reg.predict_proba(x)[:, 1][0], 4) * 100


def heat_map():
    fig, ax = plt.subplots(figsize=(8, 8))
    heatmap = sb.heatmap(data_set[['age', 'hypertension', 'heart_disease', 'avg_glucose_level',
                                   'bmi', 'smoking_status', 'stroke']].corr(), cmap="Blues", vmax=1, annot=True, ax=ax)
    plt.savefig('static/img/hm.png')
    return heatmap
