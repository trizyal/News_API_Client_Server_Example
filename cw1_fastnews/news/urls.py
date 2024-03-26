from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.view_login, name='login'),
    path('api/logout/', views.view_logout, name='logout'),
    path('api/stories/', views.post_story, name='stories'),
]
