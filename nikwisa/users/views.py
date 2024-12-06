from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Message, Like
from .serializers import CustomUserSerializer, MessageSerializer, LikeSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

# Create your views here.
