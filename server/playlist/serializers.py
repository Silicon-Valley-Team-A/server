from rest_framework import serializers
from .models import *

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields='__all__'
        #fields = ('id','title','artist','duration','file','title_album','image_album')
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =Category
        fields = ('id','keyword')

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id','user','name','tag')

class SonglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songlist
        fields = ('id','playlist','song','num')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','id','password','name')