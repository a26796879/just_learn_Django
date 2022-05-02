from celery import Celery
import time
import requests
import urllib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
app = Celery('tasks', broker='amqp://niceguy:niceguy@35.227.175.4:5672')
app.conf.update(worker_pool_restarts=True)

post_api_url = 'http://34.105.13.75/news/'
check_exist_url = 'http://34.105.13.75/news_filter/?name='
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

@app.task
def send_email(email, token):
    print ("sending email...")
    print ("you can saving a file or log a message here to verify it.")

@app.task
def add(x, y):
    return x + y

@app.task
def post_data():
    ip_url = 'https://api.myip.com/'
    res = requests.get(ip_url).json()
    post_api_url = 'http://34.105.13.75/news/'
    data = {
        "name":res['ip'],
        "publisher":res['country'],
        "url":"https://www.google.com",
        "date":"2022-04-27T20:00:00Z",
        "keyword":res['cc']
    }
    try:
        res = requests.post(post_api_url,data=data)
        return res.json()
    except Exception as exc:
        raise app.Task.retry(exc=exc, countdown=3)
    
@app.task
def get_udn_news(keyword):
    udn_url = 'https://udn.com/api/more?page=0&id=search:'+ urllib.parse.quote_plus(keyword) +'&channelId=2&type=searchword'
    res = requests.get(url=udn_url,headers=headers)
    news = res.json()['lists']
    for i in range(len(news)):
        dateString = news[i]['time']['date']
        dateFormatter = "%Y-%m-%d %H:%M:%S"
        published_date = datetime.strptime(dateString, dateFormatter)
        title = news[i]['title']
        url = news[i]['titleLink']
        data = {
            "name":title,
            "publisher":'udn聯合新聞網',
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_apple_news(keyword):
    apple_url = 'https://tw.appledaily.com/pf/api/v3/content/fetch/search-query?query=%7B%22searchTerm%22%3A%22'+ urllib.parse.quote_plus(keyword) +'%22%2C%22start%22%3A0%7D&_website=tw-appledaily'
    res = requests.get(url=apple_url,headers=headers)
    news = res.json()['content']
    for i in range(len(news)):
        dateString = news[i]['pubDate']
        published_date = (datetime.fromtimestamp(int(dateString)))
        title = news[i]['title']
        url = news[i]['sharing']['url']
        publisher = news[i]['brandName']
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_setn_news(keyword):
    url = 'https://www.setn.com/search.aspx?q='+ urllib.parse.quote_plus(keyword) +'&r=0'
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('div.newsimg-area-text-2')
    url_tag = soup.select("div.newsimg-area-info >  a.gt ")
    dates = soup.select('div.newsimg-date')
    images = soup.select('img.lazy')
    publisher = '三立新聞網'
    for i in range(len(titles)):
        title = titles[i].text
        dateString = dates[i].text
        url = 'https://www.setn.com/' + url_tag[i].get('href').replace('&From=Search','')
        image = images[i].get('data-original').replace('-L','-PH')
        dateFormatter = "%Y/%m/%d %H:%M"
        published_date = datetime.strptime(dateString, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_ettoday_news(keyword):
    url = 'https://www.ettoday.net/news_search/doSearch.php?search_term_string='+ urllib.parse.quote_plus(keyword)
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('h2 > a')
    date = soup.select('span.date')
    images = soup.select('img')
    publisher = 'ETtoday新聞雲'
    for i in range(len(titles)):
        title = titles[i].text
        url = titles[i].get('href')
        publish = date[i].text.split('/')[1].replace(' ','')
        image = 'https:' + images[i].get('src').replace('/b','/d')
        dateFormatter = "%Y-%m-%d%H:%M)"
        published_date = datetime.strptime(publish, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_TVBS_news(keyword):
    url = 'https://news.tvbs.com.tw/news/searchresult/'+ urllib.parse.quote_plus(keyword) +'/news'
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('h2.search_list_txt')
    urls = soup.select('span.search_list_box > a')
    dates = soup.select('span.publish_date')
    images = soup.select('img.lazyimage')
    publisher = 'TVBS新聞網'
    for i in range(len(titles)):
        title = titles[i].text
        url = urls[i].get('href')
        publish = dates[i].text
        image = images[i].get('data-original')
        dateFormatter = "%Y/%m/%d %H:%M"
        published_date = datetime.strptime(publish, dateFormatter)
        expect_time = datetime.today() - timedelta(hours=8)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_china_news(keyword):
    url = 'https://www.chinatimes.com/search/'+ urllib.parse.quote_plus(keyword) +'?chdtv'
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('h3 > a')
    dates = soup.select('time')
    publisher = '中時新聞網'
    images = soup.select('img.photo')
    for i in range(len(titles)):
        title = titles[i].text
        url = titles[i].get('href')
        dateString = dates[i].get('datetime')
        dateFormatter = "%Y-%m-%d %H:%M"
        published_date = datetime.strptime(dateString, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_storm_news(keyword):
    url = 'https://www.storm.mg/site-search/result?q='+ urllib.parse.quote_plus(keyword) +'&order=none&format=week'
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('p.card_title')
    urls = soup.select('a.card_substance')
    publish_dates = soup.select('span.info_time')
    images = soup.select('img.card_img')
    publisher = '風傳媒'
    for i in range(len(titles)):
        title = titles[i].text
        url = 'https://www.storm.mg' + urls[i].get('href')
        image = images[i].get('src').replace('150x150','800x533')
        publish_date = publish_dates[i].text
        dateFormatter = "%Y-%m-%d %H:%M"
        published_date = datetime.strptime(publish_date, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_ttv_news(keyword):
    url = 'https://news.ttv.com.tw/search/' + urllib.parse.quote_plus(keyword)
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('ul > li > a.clearfix > div.content > div.title')
    urls = soup.select('ul > li > a.clearfix')
    publishes = soup.select('ul > li > a.clearfix > div.content > div.time')
    publisher = '台視新聞網'
    for i in range(len(urls)):
        url = 'https://news.ttv.com.tw/'+urls[i].get('href')
        title = titles[i].text.replace('\u3000',' ') #將全形space取代為半形space
        publish = publishes[i].text
        dateFormatter = "%Y/%m/%d %H:%M:%S"
        published_date = datetime.strptime(publish, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_ftv_news(keyword):
    url = 'https://www.ftvnews.com.tw/search/' + urllib.parse.quote_plus(keyword)
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('div.title')
    urls = soup.select('ul > li > a.clearfix')
    publishes = soup.select('div.time')
    images = soup.select('img[loading]')
    publisher = '民視新聞網'
    for i in range(len(urls)):
        url = 'https://www.ftvnews.com.tw/'+urls[i].get('href')
        title = titles[i].text
        publish = publishes[i].text
        image = images[i].get('src')
        dateFormatter = "%Y/%m/%d %H:%M:%S"
        published_date = datetime.strptime(publish, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_cna_news(keyword):
    url = 'https://www.cna.com.tw/search/hysearchws.aspx?q=' + urllib.parse.quote_plus(keyword)
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    urls = soup.select('ul.mainList > li > a')
    titles = soup.select('div.listInfo > h2')
    dates = soup.select('div.date')
    publisher = 'CNA中央社' 
    for i in range(len(urls)):
        url = urls[i].get('href')
        title = titles[i].text
        publish = dates[i].text
        image_url = urls[i].img
        if image_url != None:
            image = image_url['data-src'].replace('/200/','/400/')
        else:
            image = None
        dateFormatter = "%Y/%m/%d %H:%M"
        published_date = datetime.strptime(publish, dateFormatter)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
@app.task
def get_ltn_news(keyword):
    url = 'https://search.ltn.com.tw/list?keyword=' + urllib.parse.quote_plus(keyword)
    res = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.find_all("a", class_="tit")
    images = soup.select('img.lazy_imgs')
    publisher = '自由時報電子報'
    for i in range(len(titles)):
        title = titles[i]['title'].replace('\u3000',' ') #將全形space取代為半形space
        url = titles[i]['href']
        res = requests.get(url=url,headers=headers, timeout = 10)
        soup = BeautifulSoup(res.text, 'html.parser')
        if 'health.ltn' in url:
            publish = soup.select('span.time')[1].text.replace('\n    ','').replace('\r','')
        elif 'ent.ltn' in url:
            publish = soup.select('time.time')[0].text.replace('\n    ','').replace('\r','')
        else:
            publish = soup.select('span.time')[0].text.replace('\n    ','').replace('\r','')
        dateFormatter = "%Y/%m/%d %H:%M"
        published_date = datetime.strptime(publish, dateFormatter)
        expect_time = datetime.today() - timedelta(hours=1)
        data = {
            "name":title,
            "publisher":publisher,
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        expect_time = datetime.today() - timedelta(hours=8)
        if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
            if published_date >= expect_time:
                requests.post(post_api_url,data=data)
            else:
                break
if __name__ == "__main__":
    get_udn_news.delay('台灣')
    get_apple_news.delay('台灣')
    get_setn_news.delay('台灣')
    get_ettoday_news.delay('台灣')
    get_TVBS_news.delay('台灣')
    get_china_news.delay('台灣')
    get_storm_news.delay('台灣')
    get_ttv_news.delay('台灣')
    get_ftv_news.delay('台灣')
    get_ltn_news.delay('台灣')
    get_ltn_news.delay('台灣')