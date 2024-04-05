from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.view_login, name='login'),
    path('api/logout', views.view_logout, name='logout'),
    path('api/stories', views.story, name='stories'),
    path('api/stories/<str:key>', views.delete, name='delete')
]
