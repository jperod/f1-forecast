import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np
import time
import sklearn
from sklearn.datasets import make_classification
from lightgbm import LGBMClassifier
from flaml import AutoML
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

################# PARAMETERS ###################
prediction_feature = "Future_Winner"
time_cross_validation_test_date_start = pd.to_datetime('2021-01-01')
################################################


df_ml = pd.read_feather(r"C:\F1-Forecast\DWH/ml_dataset_race_predictions")

#Prediction Targets
df_ml["Future_Winner"] = np.where(df_ml["Future_Rank"] == 1, 1, 0)
df_ml["Future_Podium"] = np.where(df_ml["Future_Rank"] <= 3, 1, 0)

#Model configuration
automl_clf = AutoML()
automl_settings = {
    "time_budget": 30,  # in seconds
    "metric": 'roc_auc',
    "task": 'classification'
    }

#time series cross validation
race_dates = list(df_ml["date"].unique())
list_y_pred = []
list_y_test = []
for race_date in race_dates:
    if race_date >= time_cross_validation_test_date_start:
        #Train Test Split
        df_ml_here = df_ml[df_ml["date"] <= race_date]
        df_ml_here = df_ml_here[[c for c in list(df_ml_here.columns) if "Future" not in c or c == prediction_feature]]

        df_train = df_ml_here[df_ml_here["date"] < race_date]
        y_train = df_train[prediction_feature]
        x_train = df_train[[c for c in list(df_train.columns) if c not in [prediction_feature, "date"]]]

        df_test = df_ml_here[df_ml_here["date"] == race_date]
        y_test = df_test[prediction_feature]
        x_test = df_test[[c for c in list(df_test.columns) if c not in [prediction_feature, "date"]]]

        # Train Model
        automl_clf.fit(x_train, y_train, **automl_settings, estimator_list=["lgbm"])
        y_pred = list(automl_clf.predict_proba(x_test)[:,1])
        list_y_pred.append(y_pred)
        list_y_test.append(y_test)

        results_here = x_test[["Driver","Team","track","season"]]
        results_here["preds"] = y_pred
        results_here["win_prob"] = [int(100*i/np.sum(y_pred)) for i in y_pred]
        results_here.sort_values(by="win_prob", ascending=False, inplace=True)
        results_here.reset_index(drop=True, inplace=True)

        print("############ Predictions Top 5 - ["+prediction_feature+"] - ############")
        print(results_here.head(5))
        print("#########################"+"#"*len(prediction_feature)+"################")

        y_pred_binary = [1 if np.argmax(list_y_pred) == i else 0 for i in range(len(list_y_pred))]

        acc = accuracy_score(y_test,y_pred)


        print(race_date)







print("END")