from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, SubCategory
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class SubCategoryViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = SubCategory.objects.all()
#         serializer = SubCategorySerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = SubCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             subcategory = SubCategory.objects.get(pk=pk)
#         except SubCategory.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = SubCategorySerializer(subcategory)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             subcategory = SubCategory.objects.get(pk=pk)
#         except SubCategory.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = SubCategorySerializer(subcategory, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             subcategory = SubCategory.objects.get(pk=pk)
#         except SubCategory.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         subcategory.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
