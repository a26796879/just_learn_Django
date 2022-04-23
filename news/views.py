from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.serializers import NewsSerializer
from .models import news_crawler
 
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'News List':'/news_list',
        'news Detail View':'/news_detail/<int:id>',
        'news Create':'/news_create',
        'news Update':'/news_update/<int:id>',
        'news Delete':'/task-delete/<int:id>'
    }
    return Response(api_urls)
    
@api_view(['GET'])
def news_list(request):
    news = news_crawler.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)
 
@api_view(['GET'])
def news_detail(request, id):
    one_news = news_crawler.objects.get(id=id)
    serializer = NewsSerializer(one_news, many=False)
    return Response(serializer.data)
