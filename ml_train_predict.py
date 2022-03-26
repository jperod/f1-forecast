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
prediction_features = ["Future_Winner", "Future_Podium", "Future_Points"]
top_n = 20
time_cross_validation_test_date_start = pd.to_datetime('2022-01-01')
################################################

df_ml = pd.read_feather(r"C:\F1-Forecast\DWH/ml_dataset_race_predictions")


#Prediction Targets
df_ml["Future_Winner"] = np.where(df_ml["Future_Rank"] == 1, 1, 0)
df_ml["Future_Podium"] = np.where(df_ml["Future_Rank"] <= 3, 1, 0)
df_ml["Future_Points"] = np.where(df_ml["Future_Rank"] <= 10, 1, 0)

#Model configuration
automl_clf = AutoML()
automl_settings = {
    "time_budget": 300,  # in seconds
    "metric": 'roc_auc',
    "task": 'classification',
    "verbose": -1
    }


#Train Test Split
race_date = df_ml["date"].max()
df_ml_here = df_ml[df_ml["date"] <= race_date]
# df_ml_here = df_ml_here[[c for c in list(df_ml_here.columns) if "Future" not in c or c == prediction_feature]]

results = []
for prediction_feature in prediction_features:
    df_train = df_ml_here[df_ml_here["date"] < race_date]
    y_train = df_train[prediction_feature]
    x_train = df_train[[c for c in list(df_train.columns) if "Future" not in c and c not in [prediction_feature, "date"]]]

    df_test = df_ml_here[df_ml_here["date"] == race_date]
    y_test = df_test[prediction_feature]
    x_test = df_test[[c for c in list(df_test.columns) if  "Future" not in c and c not in [prediction_feature, "date"]]]

    # Train Model
    automl_clf.fit(x_train, y_train, **automl_settings, estimator_list=["lgbm"])
    y_pred = list(automl_clf.predict_proba(x_test)[:,1])

    results_here = x_test.copy()[["Driver","Team","track","season"]]
    results_here["score"] = y_pred
    if prediction_feature == "Future_Winner":
        n_chances = 1
    if prediction_feature == "Future_Podium":
        n_chances = 3
    if prediction_feature == "Future_Points":
        n_chances = 10
    results_here[prediction_feature.split("_")[-1]+"_prob"] = [min(int(100*n_chances*i/np.sum(y_pred)), 100) for i in y_pred]
    results_here["Future_Rank"] = df_test["Future_Rank"]
    results_here.sort_values(by="score", ascending=False, inplace=True)
    results_here.reset_index(drop=True, inplace=True)
    results_here.index = np.arange(1, len(results_here) + 1)
    results_here["RankAcc"] = np.where(results_here["Future_Rank"] <= results_here.index, 1, 0)
    print("\n########### PREDICTING " + list(x_test["track"])[0] + " - " + str(list(x_test["season"])[0]) + " ###########" )
    print("### Predictions Top "+str(top_n)+" - ["+prediction_feature+"] - ###")

    print(results_here[["Driver", "Team", "score", prediction_feature.split("_")[-1]+"_prob", "Future_Rank"]].head(top_n))

    print("#########################"+"#"*len(prediction_feature)+"######################\n")
    print("")

    results.append(results_here)


results[0].rename(inplace=True, columns={"score": "winner_score", "Winner_prob": "winner_prob"})
results[1].rename(inplace=True, columns={"score": "podium_score", "Podium_prob": "podium_prob"})
results[2].rename(inplace=True, columns={"score": "points_score", "Points_prob": "points_prob"})
results_final = results[0]
results_final.drop(inplace=True, columns=["Future_Rank", "RankAcc"])

results_final = pd.merge(results_final, results[1][["podium_score", "podium_prob", "Driver"]], how="left", on="Driver")
results_final = pd.merge(results_final, results[2][["points_score", "points_prob", "Driver"]], how="left", on="Driver")

results_final["final_score"] = results_final["winner_score"] * results_final["podium_score"] * (results_final["points_score"]*3/10)

results_final.sort_values(by="final_score", inplace=True, ascending=False)
results_final.index = np.arange(1, len(results_here) + 1)

print(results_final[["Driver", "Team", "winner_prob", "podium_prob", "points_prob", "final_score"]].head(top_n))

print("\nPred Rank | Driver |  Team | Win Prob (%) | Podium Prob (%) | Points Prob (%) | Final Score (0-1) | Actual Rank | Prediction Result ")
print(" --- | --- | --- | --- |  --- | --- | --- | --- | --- | ")
for idx, row in results_final.iterrows():


    print(str(idx) + " | " + str(row["Driver"]) + " | " + str(row["Team"]) + " | " + str(row["winner_prob"])
          + " | " + str(row["podium_prob"]) + " | " + str(row["points_prob"]) + " | " + str(round(row["final_score"], 4)) + " | " + " | "  )


print("END")