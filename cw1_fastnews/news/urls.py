from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.funcLogin, name='login'),
    path('api/logout/', views.funcLogout, name='logout'),
]
