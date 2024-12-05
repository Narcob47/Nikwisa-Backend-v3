from django.urls import path
from weddings.views import WeddingsCategoryViewSet, WeddingSubCategoryViewSet, WeddingsViewSet
from categories.views import CategoryViewSet, SubCategoryViewSet
from store.views import StoreViewSet

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
    path(
        'categories/', CategoryViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'categories/<int:pk>/', CategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })
    ),
    path(
        'subcategories/', SubCategoryViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'subcategories/<int:pk>/', SubCategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })
    ),
    
    path (
        'store_list', StoreViewSet.as_view({
        'get': 'list',
        'post': 'create'
        })
    ),

    path(
        'store_list/<int:pk>/', StoreViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
        })
    ),
]