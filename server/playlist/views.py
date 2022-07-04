from msilib.schema import Error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

def save(request):

    if success: # 프론트에서 ajax 쓰면 그에 응답으로 바뀔 수 있음
        return HttpResponse('success')