# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 13:29:29 2021

@author: hank8
"""
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymysql
from sqlalchemy import create_engine
import datetime

pymysql.install_as_MySQLdb()

url = requests.get("https://dailyview.tw/")
sp = BeautifulSoup(url.text,"html.parser")
def daily_news():
    news_stored = []
    date_stored = []
    tought_rate_stored = []
    internet_news_stored = []
    posts = sp.find_all("div", class_="text_wrap")
    for post in posts:
        try:
            news_stored.append(post.find("h4").string.strip().replace('\u3000',''))
        except:
            news_stored.append(np.nan)
        try:
            date_stored.append(post.find("time").string.strip())
        except:
            date_stored.append(np.nan)
        try:
            internet_news_stored.append(post.find("p").string.strip().replace('\u3000',''))
        except:
            internet_news_stored.append(np.nan)
        try:
            tought_rate_stored.append(post.find("span").string.strip().replace("點閱",""))
        except:
            tought_rate_stored.append(np.nan)
    print(tought_rate_stored)
    
    daily_news_dict ={"news": news_stored,
                "news_touch_rate": tought_rate_stored,
                "internet_news": internet_news_stored,
                "date": date_stored           
    }
    daily_news_df = pd.DataFrame(daily_news_dict)
    print(daily_news_df)
  daily_news()
