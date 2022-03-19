import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np
import time

fact_practices = pd.read_feather(r"C:\F1-Forecast\DWH\fact_practices.ftr")
fact_practices["season"] = [pd.to_datetime(d).year for d in list(fact_practices["date"])]
fact_qualifying = pd.read_feather(r"C:\F1-Forecast\DWH\fact_qualifying.ftr")
fact_qualifying["season"] = [pd.to_datetime(d).year for d in list(fact_qualifying["date"])]
fact_races = pd.read_feather(r"C:\F1-Forecast\DWH\fact_races.ftr")
fact_races["season"] = [pd.to_datetime(d).year for d in list(fact_races["date"])]

valid_race_dates = list(fact_races["date"].unique())
valid_race_dates.sort()

cat_seasons = list(set([pd.to_datetime(d).year for d in valid_race_dates]))
cat_drivers = list(set(list(fact_practices["Driver"].unique()) + list(fact_qualifying["Driver"].unique()) + list(fact_races["Driver"].unique())))
cat_tracks = list(set(list(fact_practices["track"].unique()) + list(fact_qualifying["track"].unique()) + list(fact_races["track"].unique())))
cat_teams = [t for t in list(set(list(fact_practices["Team"].unique()) + list(fact_qualifying["Team"].unique()) + list(fact_races["Team"].unique()))) if t is not None]

# te
# fact_practices = fact_practices[fact_practices["Driver"] == "Max Verstappen"]
# fact_qualifying = fact_qualifying[fact_qualifying["Driver"] == "Max Verstappen"]
# fact_races = fact_races[fact_races["Driver"] == "Max Verstappen"]

data_ml = []
for i, date in enumerate(valid_race_dates):

    fact_races_loading = fact_races[fact_races["date"] <= date]
    fact_practices_loading = fact_practices[fact_practices["date"] <= date]
    fact_qualifying_loading = fact_qualifying[fact_qualifying["date"] <= date]

    print("Transforming: " + str(date))
    #Predicting goal
    fact_races_now = fact_races_loading[fact_races_loading["date"] == date]
    season = list(fact_races_now["season"].unique())[0]
    track = list(fact_races_now["track"].unique())[0]
    df_loading = fact_races_now[["Rank", "PointsPts", "Driver", "Team", "date", "track", "season"]]
    df_loading.rename(inplace=True, columns={"Rank": "Future_Rank", "PointsPts": "Future_Points"})

    #Last Practice
    fact_practices_now = fact_practices_loading[(fact_practices_loading["track"] == track) & (fact_practices_loading["season"] == season)]
    fact_practices_now.drop(columns=["date", "results_type", "Fastest Lap"], inplace=True)
    list_pivot_columns = ["Rank", "Laps", "practice_number", "time_diff_s", "time_diff_ms"]
    list_nonpivot_columns = [c for c in list(fact_practices_now.columns) if c not in list_pivot_columns]
    for pn in list(fact_practices_now["practice_number"]):
        fact_practices_now[["p"+str(pn)+"_"+c for c in list_pivot_columns]] = fact_practices_now.loc[fact_practices_now["practice_number"]==pn, list_pivot_columns]
    fact_practices_now = fact_practices_now[[c for c in list(fact_practices_now.columns) if c not in list_pivot_columns ]]
    fact_practices_now = fact_practices_now.groupby(list_nonpivot_columns)[list(fact_practices_now.columns)].agg('max') #pd.DataFrame(fact_practices_now.max(axis=0)).T
    fact_practices_now.reset_index(drop=True, inplace=True)
    df_loading = pd.merge(df_loading, fact_practices_now, how="left", on=["Driver", "Team", "track", "season"])

    #Last Qualifying
    fact_qualifying_now = fact_qualifying_loading[(fact_qualifying_loading["track"] == track) & (fact_qualifying_loading["season"] == season)]
    fact_qualifying_now.drop(columns=["date", "results_type", "Qualifying 1Q1", "Qualifying 2Q2", "Qualifying 3Q3", "Time", "BestTime"], inplace=True)
    df_loading = pd.merge(df_loading, fact_qualifying_now, how="left", on=["Driver", "Team", "track", "season"])

    assert df_loading.isnull().values[df_loading.isnull().values == True].size / df_loading.size < 0.10

    data_ml.append(df_loading)
    # print("db")

df_ml = pd.concat(data_ml)
df_ml["season"] = pd.Categorical(df_ml["season"], categories=cat_seasons)
df_ml["Driver"] = pd.Categorical(df_ml["Driver"], categories=cat_drivers)
df_ml["track"] = pd.Categorical(df_ml["track"], categories=cat_tracks)
df_ml["Team"] = pd.Categorical(df_ml["Team"], categories=cat_teams)
# cat_seasons = list(set([pd.to_datetime(d).year for d in valid_race_dates]))
# cat_drivers = list(set(list(fact_practices["Driver"].unique()) + list(fact_qualifying["Driver"].unique()) + list(fact_races["Driver"].unique())))
# cat_tracks = list(set(list(fact_practices["track"].unique()) + list(fact_qualifying["track"].unique()) + list(fact_races["track"].unique())))
# cat_teams = list(set(list(fact_practices["Team"].unique()) + list(fact_qualifying["Team"].unique()) + list(fact_races["Team"].unique())))


df_ml.reset_index(drop=True, inplace=True)
df_ml.to_feather(r"C:\F1-Forecast\DWH/ml_dataset_race_predictions")


print("END")