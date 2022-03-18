import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np
import time

def remove_duplicates_from_col(df, colname):
    if list(df[colname])[0][0:int(len(list(df[colname])[0]) / 2)] == list(df[colname])[0][int(len(list(df[colname])[0]) / 2):]:
        df[colname] = [r[0:int(len(r) / 2)] for r in df[colname]]
    return df

data_practices = []
data_qualifying = []
data_races = []
for year in [str(n) for n in [2022, 2021, 2020, 2019, 2018]]:
    if year < '2023':
        url = "https://www.bbc.com/sport/formula1/"+year+"/results"
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        list_of_races = [e.contents[0].text for e in soup.find_all('button') if e.contents[0].text != '']
        list_of_races.reverse()
        list_of_grand_prix_dates = [e[e.index( str([int(i) for i in e if i.isdigit() ][0]) ) : ] for e in list_of_races]
        list_of_grand_prix_dates = [gpd.split("Grand Prix")[-1] if "Grand Prix" in gpd else gpd for gpd in list_of_grand_prix_dates]
        list_of_grand_prix = [ "70th-anniversary-grand-prix" if e == 'Formula 1 70th Anniversary Grand Prix, SilverstoneFormula 1 70th Anniversary Grand Prix9 August 2020' else e[ : e.index( str([int(i) for i in e if i.isdigit() ][0]) ) ].split(",")[0] for e in list_of_races]
        list_of_grand_prix = [t[0:int(len(t)/2)] if t[0:int(len(t)/2)] == t[int(len(t)/2):] else t for t in list_of_grand_prix] #remove duplications

        print(year)
        assert len(list_of_grand_prix) == len(list_of_grand_prix_dates)
        for i, grand_prix in enumerate(list_of_grand_prix):
            grand_prix_date = pd.to_datetime(list_of_grand_prix_dates[i])
            grand_prix_url_name = grand_prix.lower().replace(" ","-")
            for results_type in ["practice", "qualifying", "race"]:
                url = "https://www.bbc.com/sport/formula1/"+year+"/"+grand_prix_url_name+"/results/" + results_type
                if results_type == "practice":

                    while True:
                        try:
                            df_gp_loading = pd.read_html(url)
                            break
                        except:
                            #wait, try again
                            time.sleep(1)
                            print("Error - can't read_html")
                            print(url)
                            print("")

                    # time.sleep(0.25)
                    n_practices = len(df_gp_loading)
                    assert n_practices <= 3
                    for p in range(n_practices):
                        if all([r.isdigit() == False for r in df_gp_loading[p]['Rank']]) or all([r == "not available-" or "Last updated" in r for r in df_gp_loading[p]['Fastest Lap']]):
                            df_gp_loading[p] = pd.DataFrame(columns=["Rank", "Driver", "Team", "Fastest Lap", "Laps", "results_type", "track", "practice_number", "date", "time_diff_s", "time_diff_ms"])
                            print("")
                        else:
                            df_gp_loading[p] = df_gp_loading[p].loc[ df_gp_loading[p]['Rank'].astype(str).str.isdigit(), ["Rank", "Driver", "Team", "Fastest Lap", "Laps"]]
                            df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Rank")
                            df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Laps")
                            df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Fastest Lap")
                            df_gp_loading[p]["Driver"] = [i[0:-3] for i in list(df_gp_loading[p]["Driver"])]
                            df_gp_loading[p]["results_type"] = results_type
                            df_gp_loading[p]["practice_number"] = n_practices-p
                            if n_practices-p == n_practices:
                                #Third Practice 1 day before
                                practice_date = grand_prix_date - datetime.timedelta(days=1)
                            else:
                                #First and Second Practices 2 days before
                                practice_date = grand_prix_date - datetime.timedelta(days=2)
                            df_gp_loading[p]["date"] = practice_date
                            df_gp_loading[p]["track"] = grand_prix
                            best_time = df_gp_loading[p].loc[0,"Fastest Lap"]
                            assert len(best_time) == 8 and all([len(t) == 8 or t == "not ava" for t in list(df_gp_loading[p]["Fastest Lap"])])
                            timediffs = [pd.to_datetime("2000-01-01 12:"+t) - pd.to_datetime("2000-01-01 12:"+best_time) if "not ava" not in t else pd.to_datetime("2000-01-01 12") - pd.to_datetime("2000-01-01 13") for t in list(df_gp_loading[p]["Fastest Lap"]) ]
                            df_gp_loading[p]["time_diff_s"] = [t.seconds for t in timediffs]
                            df_gp_loading[p]["time_diff_ms"] = [int(t.delta/1000000) for t in timediffs]
                            # print("")

                    if n_practices == 3:
                        df_gp_loading = pd.concat([df_gp_loading[0], df_gp_loading[1], df_gp_loading[2]], axis=0)
                    elif n_practices == 2:
                        df_gp_loading = pd.concat([df_gp_loading[0], df_gp_loading[1]], axis=0)
                    elif n_practices == 1:
                        df_gp_loading = pd.concat([df_gp_loading[0]], axis=0)
                    df_gp_loading["Rank"] = df_gp_loading["Rank"].astype(int)
                    df_gp_loading["Laps"] = [int(d.replace("not ava","0")) for d in df_gp_loading["Laps"]]
                    df_gp_loading["Laps"] = df_gp_loading["Laps"].astype(int)
                    data_practices.append(df_gp_loading)

                elif results_type == "qualifying":
                    df_gp_loading = pd.read_html(url)
                    n_quals = len(df_gp_loading)
                    assert n_quals <= 2
                    if df_gp_loading[0].shape[0] > 0:
                        for p in range(1):
                            if all([r.isdigit() == False for r in df_gp_loading[p]['Rank']]) or all(
                                    [r == "not available-" or "Last updated" in r for r in
                                     df_gp_loading[p]['Qualifying 1Q1']]):
                                df_gp_loading[p] = pd.DataFrame(
                                    columns=["Rank", "Driver", "Team","Qualifying 1Q1","Qualifying 2Q2","Qualifying 3Q3","Time", "track", "IsBestQ1", "IsBestQ2", "IsBestQ3", "BestTime", "RankQ1", "RankQ2", "RankQ3", "AvgQRank", "date", "time_diff_s", "time_diff_ms"])
                                print("")
                            else:
                                df_gp_loading[p] = df_gp_loading[p].loc[df_gp_loading[p]['Rank'].astype(str).str.isdigit(), ["Rank", "Driver", "Team","Qualifying 1Q1","Qualifying 2Q2","Qualifying 3Q3","Time"]]
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Rank")
                                df_gp_loading[p]["Driver"] = [i[0:-3] for i in list(df_gp_loading[p]["Driver"])]
                                df_gp_loading[p]["results_type"] = results_type
                                df_gp_loading[p]["IsBestQ1"] = np.where(df_gp_loading[p]["Qualifying 1Q1"].str.contains("countdownfastest"), 1, 0)
                                df_gp_loading[p]["Qualifying 1Q1"] = [t.replace("countdownfastest lap ", "") for t in list(df_gp_loading[p]["Qualifying 1Q1"])]
                                df_gp_loading[p]["IsBestQ2"] = np.where(df_gp_loading[p]["Qualifying 2Q2"].str.contains("countdownfastest"), 1, 0)
                                df_gp_loading[p]["Qualifying 2Q2"] = [t.replace("countdownfastest lap ", "") for t in list(df_gp_loading[p]["Qualifying 2Q2"])]
                                df_gp_loading[p]["IsBestQ3"] = np.where(df_gp_loading[p]["Qualifying 3Q3"].str.contains("countdownfastest"), 1, 0)
                                df_gp_loading[p]["Qualifying 3Q3"] = [t.replace("countdownfastest lap ", "") for t in list(df_gp_loading[p]["Qualifying 3Q3"])]
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Qualifying 1Q1")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Qualifying 2Q2")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Qualifying 3Q3")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Time")
                                df_gp_loading[p]["BestTime"] = df_gp_loading[p][["Qualifying 1Q1", "Qualifying 2Q2", "Qualifying 3Q3"]].min(axis=1)
                                df_gp_loading[p]["RankQ1"] = df_gp_loading[p]['Qualifying 1Q1'].rank(ascending=True).astype(int)
                                df_gp_loading[p]["RankQ2"] = np.where ( df_gp_loading[p]["Qualifying 2Q2"].str.contains("not"), -1 ,df_gp_loading[p]['Qualifying 2Q2'].rank(ascending=True)).astype(int)
                                df_gp_loading[p]["RankQ3"] = np.where ( df_gp_loading[p]["Qualifying 3Q3"].str.contains("not"), -1 ,df_gp_loading[p]['Qualifying 3Q3'].rank(ascending=True)).astype(int)
                                df_gp_loading[p]["AvgQRank"] = (df_gp_loading[p]["RankQ1"] + np.where ( df_gp_loading[p]["Qualifying 2Q2"].str.contains("not"), 0 ,1)*df_gp_loading[p]["RankQ2"]  + np.where ( df_gp_loading[p]["Qualifying 3Q3"].str.contains("not"), 0 ,1)*df_gp_loading[p]["RankQ3"]) / ( 1 + np.where ( df_gp_loading[p]["Qualifying 2Q2"].str.contains("not"), 0 ,1) + np.where ( df_gp_loading[p]["Qualifying 3Q3"].str.contains("not"), 0 ,1) )

                                best_time = df_gp_loading[p].loc[0,"BestTime"]
                                timediffs = [pd.to_datetime("2000-01-01 12:"+t) - pd.to_datetime("2000-01-01 12:"+best_time) if "not ava" not in t else pd.to_datetime("2000-01-01 12") - pd.to_datetime("2000-01-01 13") for t in list(df_gp_loading[p]["BestTime"]) ]
                                df_gp_loading[p]["time_diff_s"] = [t.seconds for t in timediffs]
                                df_gp_loading[p]["time_diff_ms"] = [int(t.delta/1000000) for t in timediffs]
                                qualifying_date = grand_prix_date - datetime.timedelta(days=1)
                                df_gp_loading[p]["date"] = qualifying_date
                                df_gp_loading[p]["track"] = grand_prix
    
    
                        if n_quals == 2:
                            df_gp_loading_sprint = df_gp_loading[1]
                            df_gp_loading = df_gp_loading[0]
                            df_gp_loading_sprint = remove_duplicates_from_col(df_gp_loading_sprint, "Rank")
                            df_gp_loading_sprint["Driver"] = [i[0:-3] for i in list(df_gp_loading_sprint["Driver"])]
                            df_gp_loading_sprint = df_gp_loading_sprint.loc[:19,["Rank", "Driver"]]
                            df_gp_loading_sprint.rename(columns={"Rank": "RankSprint"}, inplace=True)
                            df_gp_loading = pd.merge(df_gp_loading, df_gp_loading_sprint, on="Driver")
                            df_gp_loading["RankSprint"] = [i if i[0].isdigit() else '-1' for i in df_gp_loading["RankSprint"] ]
                            df_gp_loading["RankSprint"] = df_gp_loading["RankSprint"].astype(int)
                        else:
                            df_gp_loading = df_gp_loading[0]
                            df_gp_loading["RankSprint"] = -1
    
                        data_qualifying.append(df_gp_loading)

                elif results_type == "race":
                    df_gp_loading = pd.read_html(url)
                    assert len(df_gp_loading) == 1
                    if df_gp_loading[0].shape[0] > 0:
                        for p in range(1):
                            if all([r.isdigit() == False for r in df_gp_loading[p]['Rank']]) or all(
                                    [r == "not available-" or "Last updated" in r for r in
                                     df_gp_loading[p]["Fastest Lap"]]):
                                df_gp_loading[p] = pd.DataFrame(
                                    columns=["Rank", "Driver", "Team", "Grid", "Pits", "Fastest Lap", "Race Time", "track", "PointsPts", "date", "results_type", "IsFastestLap", "IsPodium", "RaceTimeDiff_s", ])
                                print("")
                            else:
                            
                                df_gp_loading[p] = df_gp_loading[p].loc[
                                    df_gp_loading[p]['Rank'].astype(str).str.isdigit(), ["Rank", "Driver", "Team",
                                                                                         "Grid", "Pits",
                                                                                         "Fastest Lap", "Race Time", "PointsPts"]]
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Rank")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "PointsPts")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Grid")
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Pits")
                                df_gp_loading[p]["Driver"] = [i[0:-3] for i in list(df_gp_loading[p]["Driver"])]
                                df_gp_loading[p]["results_type"] = results_type
                                df_gp_loading[p]["IsFastestLap"] = np.where(df_gp_loading[p]["Fastest Lap"].str.contains("countdownfastest"), 1, 0)
                                df_gp_loading[p]["Fastest Lap"] = [t.replace("countdownfastest overall lap ", "") for t in list(df_gp_loading[p]["Fastest Lap"])]
                                df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Fastest Lap")
                                df_gp_loading[p]["IsPodium"] = np.where(df_gp_loading[p]["Rank"].astype(int) <= 3, 1, 0)
                                df_gp_loading[p]["Race Time"] = np.where(df_gp_loading[p]["Race Time"].str.contains("behind+"), [t.split("behind+")[0] + " " + "behind+" for t in df_gp_loading[p]["Race Time"]], df_gp_loading[p]["Race Time"])
                                df_gp_loading[p].loc[0,"Race Time"] = df_gp_loading[p].loc[0,"Race Time"][0:int(len(df_gp_loading[p].loc[0,"Race Time"])/2)]
                                df_gp_loading[p]["RaceTimeDiff_s"] = 1
                                best_time = df_gp_loading[p].loc[0,"Race Time"]
                                timediffs = pd.Series(np.where(df_gp_loading[p]["Race Time"].str.contains("behind +"), [t.split("behind+")[0]  for t in df_gp_loading[p]["Race Time"]], df_gp_loading[p]["Race Time"]))
                                timediffs.loc[0] = '0'
                                timediffs_s = [-1 if "no time" in t else  int(t) for t in [ '100' if 'behind' in t else t for t in [str(int(t.split(".")[0].split(":")[1]) + int(t.split(".")[0].split(":")[0])*60) if ":" in t else t.split(".")[0] for t in timediffs]]]
                                df_gp_loading[p]["RaceTimeDiff_s"] = timediffs_s
                                df_gp_loading[p]["date"] = grand_prix_date
                                df_gp_loading[p]["track"] = grand_prix
                                df_gp_loading[p]["Rank"] = df_gp_loading[p]["Rank"].astype(int)
                        df_gp_loading = df_gp_loading[0]
                        data_races.append(df_gp_loading)

                        # print("db")


                print("Sucessfully extracted <" + results_type + "> data from the <" + grand_prix + "> of <" + year + ">.")
            # print("db")


df_practices = pd.concat(data_practices)
df_practices.reset_index(inplace=True)
df_practices.to_feather(r"C:/F1-Forecast/DWH/fact_practices.ftr")
df_qualifying = pd.concat(data_qualifying)
df_qualifying.reset_index(inplace=True)
df_practices.to_feather(r"C:/F1-Forecast/DWH/fact_qualifying.ftr")
df_races = pd.concat(data_races)
df_races.reset_index(inplace=True)
df_practices.to_feather(r"C:/F1-Forecast/DWH/fact_races.ftr")

print("END")