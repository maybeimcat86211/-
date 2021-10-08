# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup 
import requests as req
import time
#-----------------------------------------------------#
'''模擬器的宣告'''
options = webdriver.FirefoxOptions()
#這邊關掉跳出通知#
options.set_preference("dom.push.enabled", False)
driver = webdriver.Firefox(options=options)
#-----------------------------------------------------#
def scroll(scroll_times_count):
    for i in range(scroll_times_count):
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        driver.execute_script(js)
        time.sleep(1)
#-----------------------------------------------------#
def login():
    #登入臉書
    driver.get("https://www.facebook.com")
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("pass")
    email.send_keys('')
    password.send_keys('')
    password.submit() 
    time.sleep(3)
login()
tags = ["柯文哲","火雞"]
url = "https://www.facebook.com/search/posts?q={}".format(tags[0])
driver.get(url)
#-----------------------------------------------------#
def get_posts():
    i = 1
    while True:
        if i == 31:
            break
        scroll(1)
        posts = driver.find_element_by_css_selector(".o7dlgrpb").text
        #print(posts)
        print("第"+str(i)+"次捲動")
        try:
            the_end = driver.find_element_by_css_selector(".oqcyycmt").text
            if the_end is not None:
                print("\n'程式碼結束'")
                break
        except:
            i+=1
    print("\n'程式碼結束'")
#-----------------------------------------------------#
get_posts()
# for i in range(len(tags)):
#     url = "https://www.facebook.com/search/posts?q={}".format(tags[i])
#     get_posts()
#-----------------------------------------------------#
driver.close()
