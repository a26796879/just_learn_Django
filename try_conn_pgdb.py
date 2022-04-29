import requests

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

print(res.json())

