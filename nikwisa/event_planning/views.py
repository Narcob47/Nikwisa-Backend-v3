from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import EventPlanningCategories, EventPlanningSubCategory
from .serializers import EventPlanningCategoriesSerializer, EventPlanningSubCategorySerializer

class EventPlanningCategoriesViewSet(viewsets.ModelViewSet):
    queryset = EventPlanningCategories.objects.all()
    serializer_class = EventPlanningCategoriesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']

    def create(self, request):
        serializer = EventPlanningCategoriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            category = EventPlanningCategories.objects.get(pk=pk)
        except EventPlanningCategories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventPlanningCategoriesSerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            category = EventPlanningCategories.objects.get(pk=pk)
        except EventPlanningCategories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventPlanningCategoriesSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            category = EventPlanningCategories.objects.get(pk=pk)
        except EventPlanningCategories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventPlanningCategoriesSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = EventPlanningCategories.objects.get(pk=pk)
        except EventPlanningCategories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventPlanningSubCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = EventPlanningSubCategory.objects.all()
        serializer = EventPlanningSubCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EventPlanningSubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            subcategory = EventPlanningSubCategory.objects.get(pk=pk)
        except EventPlanningSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventPlanningSubCategorySerializer(subcategory)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            subcategory = EventPlanningSubCategory.objects.get(pk=pk)
        except EventPlanningSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventPlanningSubCategorySerializer(subcategory, data=request.data, partial=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            subcategory = EventPlanningSubCategory.objects.get(pk=pk)
        except EventPlanningSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

