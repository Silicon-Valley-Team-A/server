from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('save/', views.save, name='save'),
    path('show/', views.show, name='show' )
]
