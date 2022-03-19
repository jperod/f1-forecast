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
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score
pd.set_option("display.max_columns", 10)

################# PARAMETERS ###################
prediction_feature = "Future_Winner"
top_n = 10
time_cross_validation_test_date_start = pd.to_datetime('2021-01-01')
################################################

df_ml = pd.read_feather(r"C:\F1-Forecast\DWH/ml_dataset_race_predictions")

#Prediction Targets
df_ml["Future_Winner"] = np.where(df_ml["Future_Rank"] == 1, 1, 0)
df_ml["Future_Podium"] = np.where(df_ml["Future_Rank"] <= 3, 1, 0)

#Model configuration
automl_clf = AutoML()
automl_settings = {
    "time_budget": 5,  # in seconds
    "metric": 'roc_auc',
    "task": 'classification',
    "verbose": 0
    }

#time series cross validation
race_dates = list(df_ml["date"].unique())
list_y_pred = []
list_y_pred_binary = []
list_y_test = []
list_accurate_ranks = []
race_cnt = 1
for i, race_date in enumerate(race_dates):
    if race_date >= time_cross_validation_test_date_start:
        #Train Test Split
        df_ml_here = df_ml[df_ml["date"] <= race_date]
        # df_ml_here = df_ml_here[[c for c in list(df_ml_here.columns) if "Future" not in c or c == prediction_feature]]

        df_train = df_ml_here[df_ml_here["date"] < race_date]
        y_train = df_train[prediction_feature]
        x_train = df_train[[c for c in list(df_train.columns) if "Future" not in c and c not in [prediction_feature, "date"]]]

        df_test = df_ml_here[df_ml_here["date"] == race_date]
        y_test = df_test[prediction_feature]
        x_test = df_test[[c for c in list(df_test.columns) if  "Future" not in c and c not in [prediction_feature, "date"]]]

        # Train Model
        automl_clf.fit(x_train, y_train, **automl_settings, estimator_list=["lgbm"])
        y_pred = list(automl_clf.predict_proba(x_test)[:,1])
        list_y_pred.extend(y_pred)
        list_y_test.extend(list(y_test))

        results_here = x_test.copy()[["Driver","Team","track","season"]]
        results_here["preds"] = y_pred
        results_here["win_prob"] = [int(100*i/np.sum(y_pred)) for i in y_pred]
        results_here["Future_Rank"] = df_test["Future_Rank"]
        results_here.sort_values(by="preds", ascending=False, inplace=True)
        results_here.reset_index(drop=True, inplace=True)
        results_here.index = np.arange(1, len(results_here) + 1)
        results_here["RankAcc"] = np.where(results_here["Future_Rank"] <= results_here.index, 1, 0)
        print("\n########### PREDICTING " + list(x_test["track"])[0] + " - " + str(list(x_test["season"])[0]) + " ###########" )
        print("### Predictions Top "+str(top_n)+" - ["+prediction_feature+"] - ###")
        print(results_here[["Driver", "Team", "preds", "win_prob", "Future_Rank", "RankAcc"]].head(top_n))

        y_pred_binary = [1 if np.argmax(y_pred) == i else 0 for i in range(len(y_pred))]
        list_y_pred_binary.extend(y_pred_binary)

        list_accurate_ranks.extend(list(results_here["RankAcc"]))
        rank_acc = round(np.sum(list_accurate_ranks) / len(list_accurate_ranks), 2)
        print("Rank-Accuracy["+str(race_cnt)+"] = " + str(round(rank_acc,2)))

        acc = accuracy_score(list_y_test, list_y_pred_binary)
        print(prediction_feature+"-Accuracy["+str(race_cnt)+"] = " + str(round(acc,2)))
        pr = precision_score(list_y_test, list_y_pred_binary)
        print(prediction_feature+"-Precision["+str(race_cnt)+"] = " + str(round(pr,2)))
        auc = roc_auc_score(list_y_test, list_y_pred)
        print(prediction_feature+"-ROC-AUC["+str(race_cnt)+"] = " + str(round(auc,2)))
        f1 = f1_score(list_y_test, list_y_pred_binary)
        print(prediction_feature+"-F1-Score["+str(race_cnt)+"] = " + str(round(f1,2)))
        race_cnt += 1

        print("#########################"+"#"*len(prediction_feature)+"######################\n")
        print("")

print("END")