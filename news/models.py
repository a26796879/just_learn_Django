from django.db import models

# Create your models here.
class news_crawler(models.Model):
    name = models.CharField(max_length=50)      # 新聞標題
    publisher = models.CharField(max_length=50) # 發布者
    url = models.URLField()                     # 連結
    date = models.DateTimeField()               # 發布時間
    keyword = models.CharField(max_length=50)   # 關鍵字