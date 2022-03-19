# f1-forecast - Using ML to Generate Weekly Predictions for F1 Races

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
* Future_Points-ROC-AUC[22] = 0.88 (Precision of predicting the points of the race)
* Future_Points-F1-Score[22] = 0.17 (Precision of predicting the points of the race)

# 2022 Season Predictions
## Prediction 1 - 2022 Bahrain Grand Prix


