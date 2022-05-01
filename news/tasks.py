from celery import Celery
import time
import requests
import urllib
from datetime import datetime, timedelta
app = Celery('tasks', broker='amqp://niceguy:niceguy@35.227.175.4:5672')
 
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
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    udn_url = 'https://udn.com/api/more?page=0&id=search:'+ urllib.parse.quote_plus(keyword) +'&channelId=2&type=searchword'
    res = requests.get(url=udn_url,headers=headers)
    news = res.json()['lists']
    for i in range(len(news)):
        dateString = news[i]['time']['date']
        dateFormatter = "%Y-%m-%d %H:%M:%S"
        published_date = datetime.strptime(dateString, dateFormatter)
        title = news[i]['title']
        url = news[i]['titleLink']
        post_api_url = 'http://34.105.13.75/news/'
        data = {
            "name":title,
            "publisher":'udn聯合新聞網',
            "url":url,
            "date":published_date,
            "keyword":keyword
        }
        try:
            res = requests.post(post_api_url,data=data)
            return res.json()
        except Exception as exc:
            raise app.Task.retry(exc=exc, countdown=3)

