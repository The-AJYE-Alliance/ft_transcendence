from django.urls import path, include
from .models import User
from rest_framework import routers, serializers, viewsets
from .serializers import UserSerializer
from . import views


urlpatterns = [
    path('users/', views.users_list),
]