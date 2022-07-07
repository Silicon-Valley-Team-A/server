from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from requests import Response
from .models import User
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

# Create your views here.


@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        isAuthenticated = User.is_authenticated

        if isAuthenticated:
            return Response({'isAuthenticated': 'success'})
        else:
            return Response({'isAuthenticated': 'error'})


@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        email = data['email']
        id = data['id']
        password = data['password']
        re_password = data['re_password']
        username = data['username']

        if password == re_password:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User already exists'})
            else:
                user = User.objects.create_user(
                    email=email,
                    id=id,
                    password=password,
                    username=username
                )
                user.save()
                return Response({'result': 'User created successfully'})
        else:
            return Response({'error': 'Passwords do not match'})


# React에서 CSRF token 받기
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
