from celery import Celery
import time
import requests

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
    res = requests.post(post_api_url,data=data)
    return res.json()

