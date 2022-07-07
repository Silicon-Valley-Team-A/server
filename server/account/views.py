from http.client import ResponseNotReady
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

# from django.contrib.auth.models import User

from .models import User
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

# Create your views here.


# 인증된 user인지 확인
@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            isAuthenticated = User.is_authenticated

            if isAuthenticated:
                return Response({'isAuthenticated': 'success'})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})


# 회원가입
@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        email = data['email']
        id = data['id']
        password = data['password']
        re_password = data['re_password']
        name = data['name']

        try:
            if password == re_password:
                if User.objects.filter(email=email).exists():
                    return Response({'error': 'User already exists'})
                else:
                    user = User(
                        email=email,
                        id=id,
                        password=password,
                        name=name
                    )
                    user.save()
                    return Response({'result': 'User created successfully'})
            else:
                return Response({'error': 'Passwords do not match'})
        except:
            return Response({'error': 'Something went wrong when registering'})


# 로그아웃
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logged out'})
        except:
            return Response({'error': 'Someting went wrond when logging out'})


# 로그인
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        id = data['id']
        password = data['password']

        try:
            user = auth.authenticate(id=id, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({'success': 'User authenticated'})
            else:
                return Response({'error': 'Error authenticating'})
        except:
            return Response({'error': 'Something went wrong when logging in'})


# React에서 CSRF token 받기
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
