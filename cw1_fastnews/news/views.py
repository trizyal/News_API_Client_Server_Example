from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Author, News

# Create your views here.

# @csrf_exempt
# def login(request):
#     if request.method == 'POST' and request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
#         u = request.POST.get('username')
#         p = request.POST.get('password')
#         try:
#             user = Author.objects.get(username=u)
#             if user.username == u and user.password == p:
#                 request.session['username'] = user.username
#                 return HttpResponse('Welcome ' + user.first_name, status=200, content_type='text/plain')
#             else:
#                 return HttpResponse('Invalid credentials', status=401, content_type='text/plain')
#         except:
#             return HttpResponse('Invalid credentials', status=401, content_type='text/plain')
#     else:
#         return HttpResponse('Invalid request', status=405, content_type='text/plain')

@csrf_exempt
def funcLogin(request):
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        u = request.POST.get('username')
        p = request.POST.get('password')
        # try:
        #     user = authenticate(username=u, password=p)
        #     login(request, user)
        #     return HttpResponse('Welcome ' + user.first_name, status=200, content_type='text/plain')
        # except:
        #     return HttpResponse('Invalid credentials', status=401, content_type='text/plain')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return HttpResponse('Welcome ' + user.first_name, status=200, content_type='text/plain')
        else:
            return HttpResponse('Invalid credentials', status=401, content_type='text/plain')
    else:
        return HttpResponse('Invalid request', status=405, content_type='text/plain')

@csrf_exempt
def funcLogout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Logged out', status=200, content_type='text/plain')
    else:
        return HttpResponse('Invalid request', status=409, content_type='text/plain')
