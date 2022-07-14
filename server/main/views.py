from email.mime import application
import json
from django.http import JsonResponse

# Create your views here.
def main(request):
    return JsonResponse({"success": True})