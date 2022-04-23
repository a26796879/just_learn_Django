from rest_framework import serializers
from .models import news_crawler

class NewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = news_crawler
    fields = ['id', 'name', 'publisher', 'url', 'date', 'keyword']