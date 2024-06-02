from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Author, News
import json
from datetime import datetime


# Function to handle login
# Accepts POST request with username and password
# Authenticates the user and logs them in
# Returns a welcome message 200 if successful
# Returns an error message 401 if unsuccessful
# Returns a method not allowed message 405 if the request method is not POST
@csrf_exempt
def view_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        try:
            user = authenticate(username=u, password=p)
            login(request, user)
            return HttpResponse('Welcome ' + user.first_name, status=200, content_type='text/plain')
        except:
            return HttpResponse('Unauthorized: Invalid credentials', status=401, content_type='text/plain')
    else:
        return HttpResponse(request.method + ': Method Not Allowed', status=405, content_type='text/plain')


# Function to handle logout
# Accepts POST request
# Logs out the user
# Returns a logged out message 200 if successful
# Returns an error message 401 if the user is not logged in
# Returns a method not allowed message 405 if the request method is not POST
@csrf_exempt
def view_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                logout(request)
            except:
                return HttpResponse('Error: Unable to logout', status=500, content_type='text/plain')
            return HttpResponse('OK: Logged out', status=200, content_type='text/plain')
        else:
            return HttpResponse('Unauthorized: You are not Logged In', status=401, content_type='text/plain')
    else:
        return HttpResponse(request.method + ': Method Not Allowed', status=405, content_type='text/plain')

#Function to handle posting and retrieving news stories
@csrf_exempt
def story(request):

    # POST request to post a news story
    # Accepts JSON data with headline, category, region and details
    # Returns a success message 200 if successful
    # Returns an error message 400 if the request has bad JSON data
    # Returns an error message 401 if the user is not logged in
    if request.method == 'POST':
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
                return HttpResponse('OK: Story Posted', status=200, content_type='text/plain')
            except:
                return HttpResponse('Error: Bad Request, Error in Payload' , status=400, content_type='text/plain')
        else:
            return HttpResponse('Unauthorized: You are not Logged In', status=401, content_type='text/plain')


    # GET request to retrieve news stories
    # Accepts query parameters story_cat, story_region and story_date
    # Returns a JSON response with news stories that match the query parameters
    # Returns an error message 500 if there is an error
    elif request.method == 'GET':
        try:
            c = request.GET.get('story_cat')
            r = request.GET.get('story_region')
            d = request.GET.get('story_date')
            if c == '*' and r == '*' and d == '*':
                news = News.objects.all()
            else:
                filter_dict = {}
                if c != '*':
                    filter_dict['category'] = c
                if r != '*':
                    filter_dict['region'] = r
                if d != '*':
                    # Convert date to correct format
                    # Date is received in as DD/MM/YYYY
                    # But the Database is in YYYY-MM-DD format
                    date_conv = datetime.strptime(d, '%d/%m/%Y').date()
                    d = date_conv.strftime('%Y-%m-%d')
                    filter_dict['date'] = d

                print(filter_dict)
                news = News.objects.filter(**filter_dict)

            response = []
            if news is None or len(news) == 0:
                return HttpResponse('No News Found', status=404, content_type='text/plain')
            for n in news:
                response.append({
                    'key': n.news_id, # Changed from 'news_id' to 'key' to match the client's expected key name
                    'headline': n.headline,
                    'story_cat': n.category,
                    'story_region': n.region,
                    'author': n.author.username,
                    'story_date': n.date.strftime('%d/%m/%Y'), # Convert date to DD/MM/YYYY string format
                    'story_details': n.details
                })
            # stories = json.dumps(response)
            return JsonResponse({"stories":response},safe=False, status=200, content_type='application/json')
        except:
            # return HttpResponse(e, status=500, content_type='text/plain')
            return HttpResponse('Error: Bad Request, Error in Payload' , status=400, content_type='text/plain')

    else:
        return HttpResponse(request.method + ': Method Not Allowed', status=405, content_type='text/plain')

# Function to handle deleting news stories
# Accepts DELETE request with a key parameter
# Deletes the news story with the key parameter
# Returns a success message 200 if successful
# Returns an error message 401 if the user is not logged in
# Returns an error message 404 if the story is not found
# Returns a method not allowed message 405 if the request method is not DELETE
@csrf_exempt
def delete(request, key):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                news = News.objects.get(news_id=key)
                if news.author.username == request.user.username:
                    news.delete()
                    return HttpResponse('OK: Story Deleted', status=200, content_type='text/plain')
                else:
                    return HttpResponse('Unauthorized: You are not the author of this story', status=401, content_type='text/plain')
            except:
                return HttpResponse('Error: Story not found', status=404, content_type='text/plain')
        else:
            return HttpResponse('Unauthorized: You are not Logged In', status=401, content_type='text/plain')
    else:
        return HttpResponse(request.method + ': Method Not Allowed', status=405, content_type='text/plain')