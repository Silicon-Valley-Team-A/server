from django.urls import path
from . import views

urlpatterns = [
    path('authenticated', views.checkAuthenticaed, name='checkAuthenticated'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('delete', views.delete, name='delete'),
    path('csrf_cookie', views.getCSRFToken, name='getCSRFToken')
]
