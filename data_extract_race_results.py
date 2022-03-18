import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np

def remove_duplicates_from_col(df, colname):
    if list(df[colname])[0][0:int(len(list(df[colname])[0]) / 2)] == list(df[colname])[0][int(len(list(df[colname])[0]) / 2):]:
        df[colname] = [r[0:int(len(r) / 2)] for r in df[colname]]
    return df

data_practices = []
data_qualifying = []
data_races = []
for year in [str(n) for n in [2022, 2021, 2020, 2019]]:
    if year < '2022':
        url = "https://www.bbc.com/sport/formula1/"+year+"/results"
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        list_of_races = [e.contents[0].text for e in soup.find_all('button') if e.contents[0].text != '']
        list_of_races.reverse()
        list_of_grand_prix_dates = [e[e.index( str([int(i) for i in e if i.isdigit() ][0]) ) : ] for e in list_of_races]
        list_of_grand_prix = [ e[ : e.index( str([int(i) for i in e if i.isdigit() ][0]) ) ].split(",")[0] for e in list_of_races]

        print(year)
        assert len(list_of_grand_prix) == len(list_of_grand_prix_dates)
        for i, grand_prix in enumerate(list_of_grand_prix):
            grand_prix_date = pd.to_datetime(list_of_grand_prix_dates[i])
            grand_prix_url_name = grand_prix.lower().replace(" ","-")
            for results_type in ["practice", "qualifying", "race"]:
                url = "https://www.bbc.com/sport/formula1/2021/"+grand_prix_url_name+"/results/" + results_type
                if results_type == "practice":
                    df_gp_loading = pd.read_html(url)
                    assert len(df_gp_loading) == 3
                    for p in range(3):
                        df_gp_loading[p] = df_gp_loading[p].loc[ df_gp_loading[p]['Rank'].astype(str).str.isdigit(), ["Rank", "Driver", "Team", "Fastest Lap", "Laps"]]
                        df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Rank")
                        df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Laps")
                        df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Fastest Lap")
                        df_gp_loading[p]["Driver"] = [i[0:-3] for i in list(df_gp_loading[p]["Driver"])]
                        df_gp_loading[p]["results_type"] = "practice"
                        df_gp_loading[p]["practice_number"] = 3-p
                        if 3-p == 3:
                            #Third Practice 1 day before
                            practice_date = grand_prix_date - datetime.timedelta(days=1)
                        else:
                            #First and Second Practices 2 days before
                            practice_date = grand_prix_date - datetime.timedelta(days=2)
                        df_gp_loading[p]["date"] = practice_date
                        best_time = df_gp_loading[p].loc[0,"Fastest Lap"]
                        timediffs = [pd.to_datetime("2000-01-01 12:"+t) - pd.to_datetime("2000-01-01 12:"+best_time) for t in list(df_gp_loading[p]["Fastest Lap"]) ]
                        df_gp_loading[p]["time_diff_s"] = [t.seconds for t in timediffs]
                        df_gp_loading[p]["time_diff_ms"] = [int(t.delta/1000000) for t in timediffs]

                    df_gp_loading = pd.concat([df_gp_loading[0], df_gp_loading[1], df_gp_loading[2]], axis=0)
                    df_gp_loading["Rank"] = df_gp_loading["Rank"].astype(int)
                    df_gp_loading["Laps"] = df_gp_loading["Laps"].astype(int)
                    data_practices.append(df_gp_loading)

                elif results_type == "qualifying":
                    df_gp_loading = pd.read_html(url)
                    assert len(df_gp_loading) == 1
                    for p in range(1):
                        df_gp_loading[p] = df_gp_loading[p].loc[df_gp_loading[p]['Rank'].astype(str).str.isdigit(), ["Rank", "Driver", "Team","Qualifying 1Q1","Qualifying 2Q2","Qualifying 3Q3","Time"]]
                        df_gp_loading[p] = remove_duplicates_from_col(df_gp_loading[p], "Rank")
                        df_gp_loading[p]["Driver"] = [i[0:-3] for i in list(df_gp_loading[p]["Driver"])]
                        df_gp_loading[p]["IsBestQ1"] = np.where("countdownfastest" in df_gp_loading[p]["Qualifying 1Q1"], 1, 0)

                    print("db")


                print("Sucessfully extracted <" + results_type + "> data from the <" + grand_prix + "> of <" + year + ">.")
                print("db")

print("END")