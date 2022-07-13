from email.mime import application
import json
from django.http import HttpResponse
from django.shortcuts import render
from sympy import content

# Create your views here.
def main(request):
    return HttpResponse("Hi there!", content_type=application/json)