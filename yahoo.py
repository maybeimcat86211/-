def yahoo():
#---------------#
    content = []
    tags = []
    publish_date = (strftime("%Y/%m/%d"))
    '''連線資訊以及要爬取的網頁元素'''
    yahoo_url = "https://tw.yahoo.com/?p=us"
    headers = {
        'content-type': 'text/html; charset=UTF-8'
    }
    response = requests.get(yahoo_url,headers=headers)
    yahoo_html = response.text
    soup = BeautifulSoup(yahoo_html,"html.parser")
    hot_searches = soup.find_all("a", class_="Td(n) Td(u):h Bdstartc(#d6d6d6) Bdstarts(s) Bdstartw(1px) Pstart(10px) Pend(10px) C(#324fe1)",limit=8)
    first_hot_searche = soup.find("a",class_="Td(n) Td(u):h Pend(10px) C(#324fe1)")
    '''合併資料'''
    if response.status_code == 200:
        #title資料整合
        for i in hot_searches:
            i = "熱搜標籤:"+i.text.strip()
            tags.append(i)
        first_hot_searche = "熱搜標籤:"+first_hot_searche.text.strip()
        tags.insert(0,first_hot_searche)
        #content資料整合
        content1 = soup.find_all("li",class_="List(n) Mb(12px) Mah(42px)")
        content2 = soup.find_all("p",class_="Mah(34px) Lh(17px) Ov(h) Mb(8px) Fz(15px) Pt(30px) Mx(12px)")
        content3 = soup.find_all("p",class_="Mah(68px) Lh(23px) Ov(h) B(12px) Fz(20px) Mb(12px) Pt(80px) Mx(14px)")
        for i in content1:
            content.append(i.text.strip().replace("／",""))
        for i in content2:
            content.append(i.text.strip().replace("／",""))
        for i in content3:
            content.append(i.text.strip().replace("／",""))
        for i in tags:
            content.append(i)
        mix ={
            "author":"Yahoo",
            "content":content,
            "publish_date":publish_date,
            "title":noData,
            "tags":noData,
            "source":"Yahoo_news",
            "page_url":yahoo_url,
            "thumbs_up":noData,
            "comment_count":noData
            }
        '''此DF上傳至MySQL'''
        df = pd.DataFrame(mix)
        try:
            #yahoo這邊停用,一次寫入資料即可(chunksize = 1000)
            pd.io.sql.to_sql(df,"web_scraper",con=engine,schema='你的資料庫',if_exists='append', index= False)
            print("資料寫入成功")
        except  Exception as e:
            print("連線錯誤:",e)
    else:
        print("連線失敗")
