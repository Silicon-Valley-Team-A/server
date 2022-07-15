from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth

from .models import User
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

# Create your views here.


# 인증된 user인지 확인
def checkAuthenticaed(self, request, format=None):
    user = self.request.user
    try:
        isAuthenticated = user.is_authenticated

        if isAuthenticated:
            return Response({'status': 'success',
                             'message': 'isAuthenticated'})
        else:
            return Response({{'status': 'error',
                              'message': 'not Authenticated'}})
    except:
        return Response({'status': 'error',
                         'message': 'Something went wrong when checking authentication status'})


# 회원가입
@method_decorator(csrf_protect, name='dispatch')
def register(request):
    if request.method == "POST":
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        name = request.POST.get('name', False)
        try:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User already exists'})
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=name
                )

                return Response({
                    'status': 'success',
                    'message': 'User created successfully',
                    # 'user_id': user.id
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Something went wrong when registering'})


# 로그아웃
def logout(request):
    if request.method == "POST":
        try:
            auth.logout(request)
            return Response({
                'status': 'success',
                'message': 'Logged out'})
        except:
            return Response({
                'status': 'error',
                'message': 'Someting went wrong when logging out'})


# 로그인
@method_decorator(csrf_protect, name='dispatch')
def login(request):
    email = request.POST.get('email', False)
    password = request.POST.get('password', False)

    if request.method == "POST":
        try:
            user = auth.authenticate(
                request, email=email, password=password)
            user_id = User.objects.get(email=email)
            if user is not None:
                auth.login(request, user)
                return Response({
                    'status': 'success',
                    'message': 'User authenticated',
                    # 'user_id': user_id
                })
            else:
                return Response({'status': 'error',
                                 'message': 'Error authenticating'})
        except:
            return Response({'status': 'error',
                             'message': 'Something went wrong when logging in'})


# user_id 넘겨주기
# def current_user(request):
#     user = request.user
#     user_id = User.objects.get(email=user.email)
#     return Response({
#         'user_id': user_id
#     })


# React에서 CSRF token 받기
@method_decorator(ensure_csrf_cookie, name='dispatch')
def getCSRFToken(request):
    return Response({
        'status': 'success',
        'message': 'CSRF cookie set'})


# 계정 삭제
def delete(self, request, format=None):
    user = self.request.user
    try:
        user = User.objects.filter(email=user.email).delete()
        return Response({
            'status': 'success',
            'message': 'User deleted successfully'
        })
    except:
        return Response({
            'status': 'error',
            'messeage': 'Something went wrong when trying to delete user'})
