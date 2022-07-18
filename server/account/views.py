from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
#from django.utils.decorators import method_decorator
from django.contrib import auth
from django.http import JsonResponse
import json
from .models import User
# Create your views here.


# 인증된 user인지 확인
def checkAuthenticaed(request):
    user = request.user
    try:
        isAuthenticated = user.is_authenticated

        if isAuthenticated:
            return JsonResponse({'status': 'success',
                                 'message': 'isAuthenticated'})
        else:
            return JsonResponse({'status': 'error',
                                 'message': 'not Authenticated'})
    except:
        return JsonResponse({'status': 'error',
                             'message': 'Something went wrong when checking authentication status'})


# 회원가입
# @method_decorator(csrf_protect, name='dispatch')
@csrf_protect
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        try:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error',
                                     'message':  'User already exists'})
            else:
                User.objects.create_user(
                    email=email,
                    password=password,
                    name=name
                )

                return JsonResponse({
                    'status': 'success',
                    'message': 'User created successfully'
                })
        except:
            return JsonResponse({
                'status': 'error',
                'message': 'Something went wrong when registering'})


# 로그아웃
def logout(request):
    if request.method == "POST":
        try:
            auth.logout(request)
            return JsonResponse({
                'status': 'success',
                'message': 'Logged out'})
        except:
            return JsonResponse({
                'status': 'error',
                'message': 'Someting went wrong when logging out'})


# 로그인
# @method_decorator(csrf_protect, name='dispatch')
@csrf_protect
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        try:
            user = auth.authenticate(
                request, email=email, password=password)
            user_id = User.objects.get(email=email).id
            if user is not None:
                auth.login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'User authenticated',
                    'user_id': user_id
                })
            else:
                return JsonResponse({'status': 'error',
                                     'message': 'Error authenticating'})
        except:
            return JsonResponse({'status': 'error',
                                 'message': 'Something went wrong when logging in'})


# React에서 CSRF token 받기
# @method_decorator(ensure_csrf_cookie, name='dispatch')
@ensure_csrf_cookie
def getCSRFToken(request):
    if request.method == "GET":
        return JsonResponse({
            'status': 'success',
            'message': 'CSRF cookie set'})


# 계정 삭제
def delete(request):
    user = request.user
    try:
        user = User.objects.filter(email=user.email).delete()
        return JsonResponse({
            'status': 'success',
            'message': 'User deleted successfully'
        })
    except:
        return JsonResponse({
            'status': 'error',
            'messeage': 'Something went wrong when trying to delete user'})
