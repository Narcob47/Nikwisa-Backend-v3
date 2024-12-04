from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WeddingsCategory, WeddingSubCategory, Weddings
from .serializers import WeddingsCategorySerializer, WeddingSubCategorySerializer, WeddingsSerializer

class WeddingsCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = WeddingsCategory.objects.all()
        serializer = WeddingsCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = WeddingsCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
