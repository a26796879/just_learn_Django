from rest_framework import serializers
from .models import news_crawler
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
class NewsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = news_crawler
    fields = ['id', 'name', 'publisher', 'url', 'date', 'keyword']
    