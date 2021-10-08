# web_crawler
各個網站的網路爬蟲程式碼參考_python
Created on Fri Jul  9 07:59:01 2021
last update on 2021/07/09
@author: 陳永瀚
"""
'''導入爬蟲所需'''
import cloudscraper
import json
from random import randint
import requests,pymysql
from bs4 import BeautifulSoup
import pandas as pd
from time import strftime
import time
from sqlalchemy import create_engine
'''MySql連線資訊'''
pymysql.install_as_MySQLdb()
DB_STRING = 'mysql+mysqldb://root:@127.0.0.1/[中括號內改成你自己的]?charset=utf8mb4'
engine = create_engine(DB_STRING)
sql = "SELECT * FROM [你的資料表];"
df_read = pd.read_sql_query(sql, engine)
#共同變數
noData = "None"
#ptt初始網址,如果要換看板,可以做更動
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
'''各網站爬蟲function集合'''
