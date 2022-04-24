from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.serializers import NewsSerializer
from .models import news_crawler


