from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
import urllib
import asyncio
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from just_learn.celery import app

post_api_url = 'http://34.105.13.75/news/'
check_exist_url = 'http://34.105.13.75/news_filter/?name='
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

NEWS_TIME_LIMIT = 8

def send_email(email, token):
    print ("sending email...")
    print ("you can saving a file or log a message here to verify it.")


def add(x, y):
    return x + y


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
    
class News:
    async def get_udn_news(keyword):
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_apple_news(keyword):
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_setn_news(keyword):
        url = 'https://www.setn.com/search.aspx?q='+ urllib.parse.quote_plus(keyword) +'&r=0'
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.newsimg-area-text-2')
        url_tag = soup.select("div.newsimg-area-info >  a.gt ")
        dates = soup.select('div.newsimg-date')
        publisher = '三立新聞網'
        for i in range(len(titles)):
            title = titles[i].text
            dateString = dates[i].text
            url = 'https://www.setn.com/' + url_tag[i].get('href').replace('&From=Search','')
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(dateString, dateFormatter)
            data = {
                "name":title,
                "publisher":publisher,
                "url":url,
                "date":published_date,
                "keyword":keyword
            }
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_ettoday_news(keyword):
        url = 'https://www.ettoday.net/news_search/doSearch.php?search_term_string='+ urllib.parse.quote_plus(keyword)
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2 > a')
        date = soup.select('span.date')
        publisher = 'ETtoday新聞雲'
        for i in range(len(titles)):
            title = titles[i].text
            url = titles[i].get('href')
            publish = date[i].text.split('/')[1].replace(' ','')
            dateFormatter = "%Y-%m-%d%H:%M)"
            published_date = datetime.strptime(publish, dateFormatter)
            data = {
                "name":title,
                "publisher":publisher,
                "url":url,
                "date":published_date,
                "keyword":keyword
            }
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_TVBS_news(keyword):
        url = 'https://news.tvbs.com.tw/news/searchresult/'+ urllib.parse.quote_plus(keyword) +'/news'
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2.search_list_txt')
        urls = soup.select('span.search_list_box > a')
        dates = soup.select('span.publish_date')
        publisher = 'TVBS新聞網'
        for i in range(len(titles)):
            title = titles[i].text
            url = urls[i].get('href')
            publish = dates[i].text
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            data = {
                "name":title,
                "publisher":publisher,
                "url":url,
                "date":published_date,
                "keyword":keyword
            }
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_china_news(keyword):
        url = 'https://www.chinatimes.com/search/'+ urllib.parse.quote_plus(keyword) +'?chdtv'
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h3 > a')
        dates = soup.select('time')
        publisher = '中時新聞網'
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_storm_news(keyword):
        url = 'https://www.storm.mg/site-search/result?q='+ urllib.parse.quote_plus(keyword) +'&order=none&format=week'
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('p.card_title')
        urls = soup.select('a.card_substance')
        publish_dates = soup.select('span.info_time')
        publisher = '風傳媒'
        for i in range(len(titles)):
            title = titles[i].text
            url = 'https://www.storm.mg' + urls[i].get('href')
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_ttv_news(keyword):
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_ftv_news(keyword):
        url = 'https://www.ftvnews.com.tw/search/' + urllib.parse.quote_plus(keyword)
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.title')
        urls = soup.select('ul > li > a.clearfix')
        publishes = soup.select('div.time')
        publisher = '民視新聞網'
        for i in range(len(urls)):
            url = 'https://www.ftvnews.com.tw/'+urls[i].get('href')
            title = titles[i].text
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
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_cna_news(keyword):
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
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            data = {
                "name":title,
                "publisher":publisher,
                "url":url,
                "date":published_date,
                "keyword":keyword
            }
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break

    async def get_ltn_news(keyword):
        url = 'https://search.ltn.com.tw/list?keyword=' + urllib.parse.quote_plus(keyword)
        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.find_all("a", class_="tit")
        publisher = '自由時報電子報'
        for i in range(len(titles)):
            title = titles[i]['title'].replace('\u3000',' ') #將全形space取代為半形space
            url = titles[i]['href']
            res = requests.get(url=url,headers=headers,timeout = 10)
            soup = BeautifulSoup(res.text, 'html.parser')
            if 'health.ltn' in url or 'sports.ltn' in url:
                publish = soup.select('span.time')[1].text.replace('\n    ','').replace('\r','')
            elif 'ent.ltn' in url:
                publish = soup.select('time.time')[0].text.replace('\n    ','').replace('\r','')
            elif 'istyle' in url:
                publish = soup.select('span.time')[0].text.split('\n')[0].replace('\n    ','').replace('\r','').replace('  ','')
            else:
                publish = soup.select('span.time')[0].text.replace('\n    ','').replace('\r','')
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            data = {
                "name":title,
                "publisher":publisher,
                "url":url,
                "date":published_date,
                "keyword":keyword
            }
            expect_time = datetime.today() - timedelta(hours=NEWS_TIME_LIMIT)
            if requests.get(check_exist_url+ urllib.parse.quote_plus(title)).json() == []:
                if published_date >= expect_time:
                    requests.post(post_api_url,data=data)
                else:
                    break
                
    # 
# def test():
#     return 'Good'

    
async def main(*keywords):
    udn_task = (News().get_udn_news(keyword) for keyword in keywords)
    apple_task = (News().get_apple_news(keyword) for keyword in keywords)
    setn_task = (News().get_setn_news(keyword) for keyword in keywords)
    ettoday_task = (News().get_ettoday_news(keyword) for keyword in keywords)
    tvbs_task = (News().get_TVBS_news(keyword) for keyword in keywords)
    china_task = (News().get_china_news(keyword) for keyword in keywords)
    storm_task = (News().get_storm_news(keyword) for keyword in keywords)
    ttv_task = (News().get_ttv_news(keyword) for keyword in keywords)
    ftv_task = (News().get_ftv_news(keyword) for keyword in keywords)
    ltn_task = (News().get_ltn_news(keyword) for keyword in keywords)
    cna_task = (News().get_cna_news(keyword) for keyword in keywords)
    result = await asyncio.gather(*udn_task,*apple_task,*setn_task,*ettoday_task,\
        *tvbs_task,*china_task,*storm_task,*ttv_task,*ftv_task,*ltn_task,*cna_task)
    return result

async def get_news(*keywords):
    asyncio.run(main(*keywords))
    

if __name__ == "__main__":
    asyncio.run(main('台灣'))