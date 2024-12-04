from django.urls import path
from weddings.views import WeddingsCategoryViewSet, WeddingSubCategoryViewSet, WeddingsViewSet

urlpatterns = [
    path(
        'weddingscategory/', WeddingsCategoryViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'weddingscategory/<int:pk>/', WeddingsCategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy',
        })
    ),
    path(
        'weddingsubcategory/', WeddingSubCategoryViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'weddingsubcategory/<int:pk>/', WeddingSubCategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy',
        })
    ),
    path(
        'weddings/', WeddingsViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'weddings/<int:pk>/', WeddingsViewSet.as_view({
            'get': 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy',
        })
    ),
]