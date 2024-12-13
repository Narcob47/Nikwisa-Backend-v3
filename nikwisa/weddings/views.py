from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeddingsCategory, WeddingSubCategory, Weddings
from .serializers import WeddingsCategorySerializer, WeddingSubCategorySerializer, WeddingsSerializer

class WeddingsCategoryViewSet(viewsets.ModelViewSet):
    queryset = WeddingsCategory.objects.all()
    serializer_class = WeddingsCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']

    def create(self, request):
        serializer = WeddingsCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            category = WeddingsCategory.objects.get(pk=pk)
        except WeddingsCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingsCategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            category = WeddingsCategory.objects.get(pk=pk)
        except WeddingsCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingsCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            category = WeddingsCategory.objects.get(pk=pk)
        except WeddingsCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingsCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = WeddingsCategory.objects.get(pk=pk)
        except WeddingsCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeddingSubCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = WeddingSubCategory.objects.all()
        serializer = WeddingSubCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = WeddingSubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            subcategory = WeddingSubCategory.objects.get(pk=pk)
        except WeddingSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingSubCategorySerializer(subcategory)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            subcategory = WeddingSubCategory.objects.get(pk=pk)
        except WeddingSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingSubCategorySerializer(subcategory, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            subcategory = WeddingSubCategory.objects.get(pk=pk)
        except WeddingSubCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeddingsViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Weddings.objects.all()
        serializer = WeddingsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = WeddingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            wedding = Weddings.objects.get(pk=pk)
        except Weddings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingsSerializer(wedding)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            wedding = Weddings.objects.get(pk=pk)
        except Weddings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WeddingsSerializer(wedding, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            wedding = Weddings.objects.get(pk=pk)
        except Weddings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        wedding.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
