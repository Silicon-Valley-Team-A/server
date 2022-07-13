from email.mime import application
import json
from django.http import HttpResponse

# Create your views here.
def main(request):
    return HttpResponse("index page")