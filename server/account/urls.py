from django.urls import path
from . import views
# from .views import CheckAuthenticatedView, SignupView, LoginView, LogoutView, DeleteAccountView, GetCSRFToken

urlpatterns = [
    path('authenticated', views.checkAuthenticaed, name='checkAuthenticated'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('delete', views.delete, name='delete'),
    path('csrf_cookie', views.getCSRFToken, name='getCSRFToken')
]

# urlpatterns = [
#     path('authenticated', CheckAuthenticatedView.as_view(),
#          name='checkAuthenticated'),
#     path('register', SignupView.as_view(), name='register'),
#     path('login', LoginView.as_view(), name='login'),
#     path('logout', LogoutView.as_view(), name='logout'),
#     path('delete', DeleteAccountView.as_view(), name='delete'),
#     path('csrf_cookie', GetCSRFToken.as_view(), name='getCSRFToken')
# ]
