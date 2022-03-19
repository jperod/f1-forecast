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

