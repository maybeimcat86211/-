# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import cloudscraper
from random import randint
import json,time
from sqlalchemy import create_engine 
import pymysql
'''MySql連線資訊'''
pymysql.install_as_MySQLdb()
DB_STRING = '你要連線的'
engine = create_engine(DB_STRING)
sql = "SELECT * FROM 你的資料庫;"
df_read = pd.read_sql_query(sql, engine)
#-----------------------------------


# 定義 CloudScraper 的實做物件
scraper = cloudscraper.create_scraper() 
'''到Dcard官方熱門文章介面後,儲存我們要的資料
例如撇取發文時間,標籤,留言總數,按讚數,作者
'''
#爬取所需要的ID以及論壇的代碼,存到url_set裡面
url_ID = []
#存論壇ID
url_Fnames = []
'''存其餘資料'''
title = []
content = []
author = []
publish_date = []
tags = []
page_url = []
thumbs_up = []
comment_count = []
#Dcard官方熱門文章介面API網址 數字可以自行更改 這邊我抓50篇
top_100_url = "https://www.dcard.tw/_api/posts?popular=true&limit=50"
#繞過反爬蟲後轉文字
top_100_page = scraper.get(top_100_url).text
#分析json文字並拿取資料
soup = BeautifulSoup(top_100_page,"html.parser")
Dcard_json  = json.loads(top_100_page)
for i in Dcard_json:
    try:
        url_ID.append((i["id"]))
        url_Fnames.append((i["forumId"]))
        thumbs_up.append((i["likeCount"]))
        comment_count.append((i["commentCount"]))
        publish_date.append((i["createdAt"][0:10]))
    except:
        pass
#合併ID以及論壇
zipped = zip(url_ID,url_Fnames)
#拿到論壇ID以及文章ID之後 ,再去該頁面爬取文章
#直接從API拿文章會不完整,固有以下程式碼去爬取完整文章
#url = "https://www.dcard.tw/f/relationship/p/236471683" #範例
#i = i+"https://www.dcard.tw/f/{}/p/{}".format(i)
counter = 1
for ID,Fname in list(zipped):
    url = "https://www.dcard.tw/f/{}/p/{}".format(Fname,ID)
    Dcard_html = (scraper.get(url).text)
    soup = BeautifulSoup(Dcard_html,"html.parser")
    #隨機睡一下 假裝成正常使用者
    time.sleep(randint(1,4))
    #page_url儲存網站網址
    page_url.append(url)
    #找作者元素
    authors = soup.find("div",class_="s3d701-2 kBmYXB")
    author.append(authors.text)
    #找標題元素並儲存
    titles = soup.find("h1")
    title.append(titles.text)
    #找內文元素
    contents = soup.find("div",class_="sc-1npvbtq-0 gfjrnD")
    content.append(contents.text.strip("\n"))
    #找tags
    tags_element = soup.find("div",class_="sc-1htot3z-0 crdNHh") 
    for i in tags_element:
        try:
            tags.append(i.text)
        except:
            tags.append("None")
    #查看進度
    print("爬取第:{}篇文章".format(counter))
    counter +=1
    
#合併資料  
mix = {
"author":author,
"title":title,
"tags":tags,
"content":content,
"publish_date":publish_date,
"thumbs_up":thumbs_up,
"comment_count":comment_count,
"page_url":page_url,
"source":"Dcard"
    }

#轉df並且丟到MySQL
df = pd.DataFrame(mix)
try:
    pd.io.sql.to_sql(df,"web_scraper",con=engine,schema='你的資料庫',if_exists='append', index= False,chunksize=1000)
    print("資料寫入成功")
except  Exception as e:
    print("連線錯誤:",e)   
