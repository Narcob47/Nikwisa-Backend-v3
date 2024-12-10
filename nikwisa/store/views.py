from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store
from .serializers import StoreSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'owner']  # Add fields you want to filter by
    search_fields = ['name', 'owner__username']  # Add fields you want to search by
    ordering_fields = ['name', 'owner']  # Add fields you want to order by

# Create your views here.
