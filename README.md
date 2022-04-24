# Using ML to Generate Grand Prix Predictions for the 2022 F1 Races

This Repo contains my take at attempting to predict the race winners and podiums live for the F1 season of 2022 as a hobby project. 
* data_extract_race_results.py - This script is responsible for data scrapping race results data and generating /DWH schema-like tables of practice, qualifying and race results.
* data_transform_ml_dataset_race_predictions.py - This script transforms extracted data into the ml_dataset format.
* ml_train_test.py - This script can be used to test the model predictions historically.
* ml_train_predict.py - This script is used to generate prediction results for the latest upcoming race.

## First Testing Results: 19/03/2022 - Training from 2018+ and Testing on the 2021 Season
### Predicting Race Winner (Top 1) and Ranking:

Example of the ranking prediction for the last race of 2021 + Winning Probabilities:
* ![image](https://user-images.githubusercontent.com/58941036/159131658-dc27a5db-8679-4417-8f7b-a5676a031fbe.png)

Testing Evaluation Measures:
* Rank-Accuracy[22] = 0.65 (Accuracy on predicting the ranking order)
* Future_Winner-Accuracy[22] = 0.95 (Accuracy of predicting the winner of the race and the non-winners)
* Future_Winner-Precision[22] = 0.59 (Precision of predicting the winner of the race)
* Future_Winner-ROC-AUC[22] = 0.89 (ROC-AUC of predicting the winner of the race)
* Future_Winner-F1-Score[22] = 0.59 (F1-Score of predicting the winner of the race)

### Predicting Race Podium (Top 3) and Ranking:

Example of the ranking prediction for the last race of 2021 + Podium Probabilities:
* ![image](https://user-images.githubusercontent.com/58941036/159131798-3320685d-7fee-443d-8748-f91a9ad1dfdc.png)

Testing Evaluation Measures:
* Rank-Accuracy[22] = 0.64 (Accuracy on predicting the ranking order)
* Future_Podium-Accuracy[22] = 0.87 (Accuracy of predicting the podium of the race and the non-podium)
* Future_Podium-Precision[22] = 0.86 (Precision of predicting the podium of the race)
* Future_Podium-ROC-AUC[22] = 0.91 (ROC-AUC of predicting the podium of the race)
* Future_Podium-F1-Score[22] = 0.43 (F1-Score of predicting the podium of the race)

### Predicting Race Points (Top 10) and Ranking:

Example of the ranking prediction for the last race of 2021 + Points Probabilities:
* ![image](https://user-images.githubusercontent.com/58941036/159131920-28dd9852-21fb-45aa-a9dc-f0feff3c1da5.png)

Testing Evaluation Measures:
* Rank-Accuracy[22] = 0.63 (Accuracy on predicting the ranking order)
* Future_Points-Accuracy[22] = 0.49 (Accuracy of predicting the points of the race and the non-points)
* Future_Points-Precision[22] = 0.95 (Precision of predicting the points of the race)
* Future_Points-ROC-AUC[22] = 0.88 (ROC-AUC of predicting the points of the race)
* Future_Points-F1-Score[22] = 0.17 (F1-Score of predicting the points of the race)

# 2022 Season Predictions
## [Date: 19/03/2022] - Prediction 1 - 2022 Bahrain Grand Prix

* Precision (Winner) = 0/1
* Precision (Podium) = 2/3
* Precision (Points) = 7/10
* Accuracy (Ranking) = 15/17 (3 DC)

Pred Rank | Driver |  Team | Win Prob (%) | Podium Prob (%) | Points Prob (%) | Final Score (0-1) | Actual Rank | Prediction Result 
 --- | --- | --- | --- | --- | --- | --- | --- | --- 
1 | Max Verstappen | Red Bull | 24 | 23 | 81 | 0.0209 | 💀 | Ranking: ❌ \Points: ❌ Podium: ❌ Winner: ❌
2 | Charles Leclerc | Ferrari | 21 | 25 | 79 | 0.0192 | 1 | Ranking: ✔️ \Points: ✔️ Podium: ✔️ Winner: ❌
3 | Lewis Hamilton | Mercedes | 10 | 16 | 78 | 0.006 | 3 | Ranking: 🎯 \Points: ✔️ Podium: ✔️
4 | Carlos Sainz Jnr | Ferrari | 6 | 23 | 80 | 0.0052 | 2 | Ranking: ✔️ \Points: ✔️ Podium: ❌
5 | Sergio Perez | Red Bull | 3 | 16 | 76 | 0.002 | 💀 | Ranking: ❌ \Points: ❌
6 | George Russell | Mercedes |  3 | 14 | 67 | 0.0014 | 4 | Ranking: ✔️ \Points: ✔️
7 | Valtteri Bottas | Alfa Romeo | 2 | 13 | 64 | 0.0011 | 6 | Ranking: ✔️ \Points: ✔️
8 | Fernando Alonso | Alpine | 2 | 13 | 68 | 0.001 | 9 | Ranking: ❌ \Points: ✔️
9 | Pierre Gasly | AlphaTauri | 2 | 13 | 63 | 0.0008 | 💀 | Ranking: ❌ \Points: ❌
10 | Esteban Ocon | Alpine | 1 | 12 | 69 | 0.0008 | 7 | Ranking: ✔️ \Points: ✔️
11 | Lando Norris | McLaren | 1 | 12 | 60 | 0.0006 | 15 | Ranking: ❌
12 | Kevin Magnussen | Haas | 1 | 13 | 51 | 0.0006 | 5 | Ranking: ✔️ \Points: ❌
13 | Yuki Tsunoda | AlphaTauri | 2 | 13 | 26 | 0.0004 | 8 | Ranking: ✔️ \Points: ❌
14 | Lance Stroll | Aston Martin | 2 | 12 | 26 | 0.0003 | 12 | Ranking: ✔️
15 | Mick Schumacher | Haas | 1 | 12 | 27 | 0.0003 | 11 | Ranking: ✔️
16 | Daniel Ricciardo | McLaren |  1 | 12 | 20 | 0.0002 | 14 | Ranking: ✔️
17 | Guanyu ZhouGuanyu Z | Alfa Romeo | 1 | 12 | 16 | 0.0002 | 10 | Ranking: ✔️ \Points: ❌
18 | Alexander Albon | Williams | 1 | 12 | 15 | 0.0002 | 13 | Ranking: ✔️
19 | Nico Hulkenberg | Aston Martin | 1 | 12 | 15 | 0.0002 | 17 | Ranking: ✔️
20 | Nicholas Latifi | Williams | 1 | 12 | 7 | 0.0001 | 16 | Ranking: ✔️

## [Date: 26/03/2022] - Prediction 2 - 2022 Saudi Arabia Grand Prix

* Precision (Winner) = 0/1
* Precision (Podium) = 3/3
* Precision (Points) = 8/10
* Accuracy (Ranking) = 12/15 (5 DC)

Pred Rank | Driver |  Team |  Win Prob (%) | Podium Prob (%) | Points Prob (%) | Final Score (0-1) | Actual Rank | Prediction Result 
 --- | --- | --- | --- | --- | --- | --- | --- | --- | 
1 | Carlos Sainz Jnr | Ferrari | 6 | 61 | 75 | 0.0136 | 3 | Ranking: ❌ \Points: ✔️ Podium: ✔️ Winner: ❌
2 | Charles Leclerc | Ferrari | 6 | 57 | 75 | 0.0132 | 2 | Ranking: 🎯 \Points: ✔️ Podium: ✔️ 
3 | Max Verstappen | Red Bull | 5 | 59 | 75 | 0.0119 | 1 | Ranking: ✔️ \Points: ✔️ Podium: ✔️ Winner: ❌
4 | Sergio Perez | Red Bull | 6 | 46 | 72 | 0.0095 | 4 | Ranking: 🎯 \Points: ✔️ 
5 | Valtteri Bottas | Alfa Romeo | 5 | 14 | 63 | 0.002 | 💀 | Ranking: ❌ \Points: ❌
6 | Fernando Alonso | Alpine | 4 | 8 | 65 | 0.0011 | 💀 | Ranking: ❌ \Points: ❌
7 | Lewis Hamilton | Mercedes | 5 | 9 | 40 | 0.0009 | 10 | Ranking: ❌ \Points: ✔️
8 | George Russell | Mercedes | 4 | 6 | 64 | 0.0008 | 5 | Ranking: ✔️ \Points: ✔️
9 | Esteban Ocon | Alpine |  4 | 5 | 68 | 0.0008 | 6 | Ranking: ✔️ \Points: ✔️
10 | Pierre Gasly | AlphaTauri |  4 | 5 | 66 | 0.0007 | 8 | Ranking: ✔️ \Points: ✔️
11 | Yuki Tsunoda | AlphaTauri |  4 | 5 | 54 | 0.0006 | 💀 | Ranking: ❌
12 | Kevin Magnussen | Haas | 4 | 4 | 53 | 0.0004 | 9 | Ranking: ✔️ \Points: ❌
13 | Lando Norris | McLaren | 4 | 2 | 58 | 0.0002 | 7 | Ranking: ✔️ \Points: ❌
14 | Daniel Ricciardo | McLaren |4 | 2 | 40 | 0.0002 | 💀 | Ranking: ❌
15 | Guanyu Zhou | Alfa Romeo | 4 | 2 | 28 | 0.0001 | 11 | Ranking: ✔️
16 | Mick Schumacher | Haas |  4 | 2 | 26 | 0.0001 | 💀 | Ranking: ❌
17 | Lance Stroll | Aston Martin | 4 | 2 | 25 | 0.0001 | 13 | Ranking: ✔️
18 | Nico Hulkenberg | Aston Martin |  4 | 2 | 16 | 0.0001 | 12 | Ranking: ✔️
19 | Alexander Albon | Williams |  4 | 2 | 15 | 0.0001 | 14 | Ranking: ✔️
20 | Nicholas Latifi | Williams |  4 | 2 | 12 | 0.0 | 💀 | Ranking: ❌

## [Date: 09/04/2022] - Prediction 3 - 2022 Australian Grand Prix

* Precision (Winner) = 0/1
* Precision (Podium) = 2/3
* Precision (Points) = 7/10
* Accuracy (Ranking) = 15/17 (3 DC)

Pred Rank | Driver |  Team | Win Prob (%) | Podium Prob (%) | Points Prob (%) | Final Score (0-1) | Actual Rank | Prediction Result 
 --- | --- | --- | --- |  --- | --- | --- | --- | --- | 
1 | Max Verstappen | Red Bull | 27 | 61 | 79 | 0.051 | 💀 | Ranking: ❌ \Points: ❌ Podium: ❌ Winner: ❌
2 | Charles Leclerc | Ferrari | 26 | 55 | 82 | 0.0452 | 1 | Ranking: ✔️ \Points: ✔️ Podium: ✔️ Winner: ❌
3 | Sergio Perez | Red Bull | 25 | 52 | 82 | 0.0419 | 2 | Ranking: ✔️ \Points: ✔️ Podium: ✔️
4 | Carlos Sainz Jnr | Ferrari | 2 | 30 | 80 | 0.0024 | 💀 | Ranking: ❌ \Points: ❌
5 | Lewis Hamilton | Mercedes | 3 | 13 | 72 | 0.0014 | 4 | Ranking: ✔️ \Points: ✔️
6 | Lando Norris | McLaren | 0 | 18 | 77 | 0.0005 | 5 | Ranking: ✔️ \Points: ✔️
7 | Fernando Alonso | Alpine | 1 | 11 | 66 | 0.0005 | 17 | Ranking: ❌ \Points: ❌
8 | Esteban Ocon | Alpine | 2 | 3 | 73 | 0.0002 | 7 | Ranking: ✔️ \Points: ✔️
9 | Daniel Ricciardo | McLaren | 1 | 3 | 66 | 0.0001 | 6 | Ranking: ✔️ \Points: ✔️
10 | George Russell | Mercedes | 0 | 5 | 68 | 0.0001 | 3 | Ranking: ✔️ \Points: ✔️ Podium: ❌
11 | Valtteri Bottas | Alfa Romeo | 0 | 5 | 48 | 0.0001 | 8 | Ranking: ✔️ \Points: ❌
12 | Pierre Gasly | AlphaTauri | 0 | 4 | 50 | 0.0001 | 9 | Ranking: ✔️ \Points: ❌
13 | Lance Stroll | Aston Martin | 0 | 3 | 43 | 0.0001 | 12 | Ranking: ✔️ 
14 | Yuki Tsunoda | AlphaTauri | 0 | 3 | 35 | 0.0 | 16 | Ranking: ❌ 
15 | Sebastian Vettel | Aston Martin | 0 | 5 | 13 | 0.0 | 💀 | Ranking: ❌
16 | Guanyu Zhou | Alfa Romeo | 0 | 3 | 18 | 0.0 | 11 | Ranking: ✔️
17 | Mick Schumacher | Haas | 0 | 3 | 13 | 0.0 | 13 | Ranking: ✔️
18 | Kevin Magnussen | Haas | 0 | 5 | 8 | 0.0 | 14 | Ranking: ✔️
19 | Alexander Albon | Williams | 0 | 3 | 10 | 0.0 | 10 | Ranking: ✔️ \Points: ❌
20 | Nicholas Latifi | Williams | 0 | 3 | 8 | 0.0 | 16 | Ranking: ✔️


## [Date: 24/04/2022] - Prediction 4 - 2022 Emilia Romagna Grand Prix

* Precision (Winner) = 1/1
* Precision (Podium) = 2/3
* Precision (Points) = 6/10
* Accuracy (Ranking) = 13/18 (2 DC)


Pred Rank | Driver |  Team | Win Prob (%) | Podium Prob (%) | Points Prob (%) | Final Score (0-1) | Actual Rank | Prediction Result 
 --- | --- | --- | --- |  --- | --- | --- | --- | --- | 
1 | Max Verstappen | Red Bull | 41 | 61 | 78 | 0.0733 | 1 | Ranking: 🎯 \Points: ✔️ Podium: ✔️ Winner: ✔️
2 | Charles Leclerc | Ferrari | 13 | 73 | 80 | 0.0289 | 6 | Ranking: ❌ \Points: ✔️ Podium: ❌
3 | Sergio Perez | Red Bull | 5 | 42 | 69 | 0.0059 | 2 | Ranking: ✔️ \Points: ✔️ Podium: ✔️
4 | Carlos Sainz Jnr | Ferrari | 7 | 24 | 77 | 0.0052 | 💀 | Ranking: ❌ \Points: ❌
5 | Lando Norris | McLaren | 3 | 26 | 69 | 0.002 | 3 | Ranking: ✔️ \Points: ✔️ Podium: ❌
6 | Fernando Alonso | Alpine | 2 | 8 | 73 | 0.0007 | 💀 | Ranking: ❌ \Points: ❌
7 | George Russell | Mercedes | 4 | 9 | 40 | 0.0006 | 4 | Ranking: ✔️ \Points: ✔️
8 | Lewis Hamilton | Mercedes | 2 | 9 | 54 | 0.0005 | 13 | Ranking: ❌ \Points: ❌
9 | Kevin Magnussen | Haas | 1 | 9 | 68 | 0.0004 | 9 | Ranking: 🎯 \Points: ✔️ 
10 | Daniel Ricciardo | McLaren | 1 | 4 | 71 | 0.0002 | 18 | Ranking: ❌ \Points: ❌
11 | Valtteri Bottas | Alfa Romeo | 1 | 6 | 57 | 0.0002 | 5 | Ranking: ✔️ \Points: ❌
12 | Guanyu Zhou | Alfa Romeo | 1 | 3 | 38 | 0.0001 | 15 | Ranking: ❌
13 | Sebastian Vettel | Aston Martin | 1 | 2 | 42 | 0.0001 | 8 | Ranking: ✔️ \Points: ❌
14 | Mick Schumacher | Haas | 1 | 3 | 32 | 0.0001 | 17 | Ranking: ❌
15 | Alexander Albon | Williams | 1 | 2 | 38 | 0.0001 | 11 | Ranking: ✔️
16 | Lance Stroll | Aston Martin | 1 | 2 | 32 | 0.0 | 10 | Ranking: ✔️ \Points: ❌
17 | Pierre Gasly | AlphaTauri | 1 | 3 | 21 | 0.0 | 12 | Ranking: ✔️
18 | Esteban Ocon | Alpine | 1 | 2 | 24 | 0.0 | 14 | Ranking: ✔️
19 | Yuki Tsunoda | AlphaTauri | 1 | 2 | 21 | 0.0 | 7 | Ranking: ✔️ \Points: ❌
20 | Nicholas Latifi | Williams | 1 | 2 | 7 | 0.0 | 16 | Ranking: ✔️



