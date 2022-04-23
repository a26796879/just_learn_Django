from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import news_crawler
from .serializers import NewsSerializer

class NewsViewSet(viewsets.ModelViewSet):
  queryset = news_crawler.objects.all()
  serializer_class = NewsSerializer
  permission_classes = (AllowAny,)