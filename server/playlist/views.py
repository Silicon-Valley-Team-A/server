from msilib.schema import Error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import *
import json
from rest_framework import generics, status
from .serializers import SongSerializer

# Create your views here.
class IndexView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
       
def save(request):
    queryset=Song.objects.all()
    reqData=request.data
    serializer=SongSerializer(data=reqData)

    if serializer.is_valid():
        serializer.save()
            #return HttpResponse('success')
