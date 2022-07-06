from msilib.schema import Error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import *

# Create your views here.

def save(request):
    p=Song(
    id='a',
    title='a',
    artist='a',
    duration=1,
    file='a',
    title_album='a',
    image_album='a')
    p.save()

    if success: # 프론트에서 ajax 쓰면 그에 응답으로 바뀔 수 있음
        return HttpResponse('success')