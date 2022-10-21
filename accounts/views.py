from django.contrib.auth import login
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User
from .serializer import RegisterSerializer

