from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Author, News
import json

# Create your views here.

@csrf_exempt
def view_login(request):
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        u = request.POST.get('username')
        p = request.POST.get('password')
        try:
            user = authenticate(username=u, password=p)
            login(request, user)
            return HttpResponse('Welcome ' + user.first_name, status=200, content_type='text/plain')
        except:
            return HttpResponse('Invalid credentials', status=401, content_type='text/plain')
    else:
        return HttpResponse('Invalid request', status=405, content_type='text/plain')

@csrf_exempt
def view_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Logged out', status=200, content_type='text/plain')
        else:
            return HttpResponse('You are not logged in', status=401, content_type='text/plain')
    else:
        return HttpResponse('Invalid request', status=409, content_type='text/plain')

@csrf_exempt
def post_story(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                headline = data.get('headline')
                print(headline)
                c = data.get('category')
                r = data.get('region')
                details = data.get('details')
                author = Author.objects.get(username=request.user.username)
                news = News(headline=headline, category=c, region=r, details=details, author=author)
                news.save()
                print(news)
            except Exception as e:
                return HttpResponse('Error: ' + str(e), status=500, content_type='text/plain')
            return HttpResponse('Story posted', status=200, content_type='text/plain')
        else:
            return HttpResponse('You are not logged in', status=401, content_type='text/plain')
    else:
        return HttpResponse('Invalid request', status=409, content_type='text/plain')
