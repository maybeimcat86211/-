#ptt初始網址,如果要換看板,可以做更動
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
def ptt_preprocess(url):
    '''帶入所需抓取的資訊'''
    headers={
        "content-type": 'text/html; charset=UTF-8',
         "cookie":"over18=1",
         "User-Agent":"輸入你自己的user-agent"
     }
    response = requests.get(url,headers=headers)
    ptt_html = response.text
    soup = BeautifulSoup(ptt_html, "html.parser")
    '''儲存資料'''
    author = [] 
    title = []  
    publish_date = [] 
    page_url = []
    thumbs_up = []
    '''抓取網頁元素並儲存'''
    posts = soup.find_all("div", class_ = "r-ent")
    for post in posts:
        try:
            author.append(post.find("div", class_ = "author").string)    
        except:
            author.append(noData)
        try:
            title.append(post.find("a").string.strip().replace("[問卦]","").replace("Fw: [情報]","").replace("Re:","").replace("[新聞]","").replace("[爆卦]","").replace("[協尋]","").replace("\u3000","").strip())
        except:
            title.append(noData)
        try:
            now_year = (strftime("%Y"))+"-"
            post = post.find("div", class_ = "date").text
            publish_date.append(now_year+post.strip())
        except:
            publish_date.append(noData)
    # 推文數藏在 div 裡面的 span 所以分開處理
    recommendations = soup.find_all("div", class_ = "nrec")
    for recommendation in recommendations:
        try:
            thumbs_up.append(int(recommendation.find("span").string))
        except:
            thumbs_up.append(noData)
    for post in posts:
        try:
            post = "https://www.ptt.cc"+str(post.find("a").get('href'))
            page_url.append(post)
        except:
            page_url.append(noData)
    #合併資料
    mix = {"author": author,
                "thumbs_up":thumbs_up,
                "title": title,
                "publish_date": publish_date,
                "page_url":page_url,
                "content":noData,
                "tags":noData,
                "source":"Ptt"
    }

    df = pd.DataFrame(mix) 
    try:
        pd.io.sql.to_sql(df,"web_scraper",con=engine,schema='寫入你的資料表',if_exists='append', index= False,chunksize=1000)
        print("資料寫入成功")
    except  Exception as e:
        print("連線錯誤:",e)    
    #抓取下一頁的連接(但在ptt裡如果要跳到下一頁,其實介面上是要按上一頁才對,所以要注意一下)
    #<a class="btn wide" href="/bbs/Gossiping/index39069.html">‹ 上頁</a>
    next_page_link = soup.find("a", string="‹ 上頁")
    #把下一頁的連接(href) return出來,丟回函式的外面
    return next_page_link["href"]
#---------------#
def ptt(url,count):
    inner_count = 1
    for i in range(count):
        print("-----------------\n目前爬蟲頁數:"+ str(inner_count)+"頁\n-----------------")
        #迴圈數到指定頁數 然後調用ptt function
        #先把page_url丟進ptt,之後return回來的href再變成page_url
        #<a class="btn wide" href="/bbs/Gossiping/index39069.html">‹ 上頁</a>
        #所以現在的page_url已經變成 https://www.ptt.cc + /bbs/Gossiping/index39069.html
        #之後以此類推 ,用for loop去跑
        url = "https://www.ptt.cc"+ptt_preprocess(url)#這邊要注意網址內容
        inner_count +=1
    print("--------\n爬蟲結束"+"\n--------")
#參數1是要爬的看板,參數2是要爬幾頁
#調用爬蟲時輸入-> ptt(url,5)
#---------------#
