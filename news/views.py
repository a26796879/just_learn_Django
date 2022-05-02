from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.serializers import NewsSerializer
from .models import news_crawler
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

class News_Filter(generics.ListAPIView):
    queryset = news_crawler.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'publisher']