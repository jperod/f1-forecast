import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np
import time

fact_practices = pd.read_feather(r"C:\F1-Forecast\DWH\fact_practices.ftr")
fact_qualifying = pd.read_feather(r"C:\F1-Forecast\DWH\fact_qualifying.ftr")
fact_races = pd.read_feather(r"C:\F1-Forecast\DWH\fact_races.ftr")



print("END")