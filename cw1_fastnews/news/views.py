from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
def story(request):
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                headline = data.get('headline')
                c = data.get('category')
                r = data.get('region')
                details = data.get('details')
                author = Author.objects.get(username=request.user.username)
                news = News(headline=headline, category=c, region=r, details=details, author=author)
                news.save()
                return HttpResponse('Story posted', status=200, content_type='text/plain')
            except Exception as e:
                return HttpResponse('Error: ' + str(e), status=500, content_type='text/plain')
        else:
            return HttpResponse('You are not logged in', status=401, content_type='text/plain')

    elif request.method == 'GET' and request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        if request.user.is_authenticated:
            try:
                c = request.GET.get("story_cat", "*")
                r = request.GET.get("story_region", "*")
                d = request.GET.get("story_date", "*")
                print(c, r, d)
                return HttpResponse('Story retrieved', status=200, content_type='text/plain')
                # news = News.objects.filter(date=d)
                # news = News.objects.all()
                # response = []
                # for n in news:
                #     response.append({
                #         'headline': n.headline,
                #         'category': n.category,
                #         'region': n.region,
                #         'author': n.author.username,
                #         'date': n.date,
                #         'details': n.details
                #     })
                # return JsonResponse({"news": response}, status=200, content_type='application/json')
            except Exception as e:
                return HttpResponse('Error: ' + str(e), status=500, content_type='text/plain')

    else:
        return HttpResponse('Invalid request', status=409, content_type='text/plain')
