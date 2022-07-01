from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('api/', views.api, name='api')
]