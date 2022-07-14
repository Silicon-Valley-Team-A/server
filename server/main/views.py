from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def main(request):
    # template_name = "index.html"
    HttpResponse("hi")