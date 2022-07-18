from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('save', views.save),
    path('playlist', views.playlist),
    path('playlist/<int:id>', views.showplaylist)
]