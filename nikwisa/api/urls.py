from django.urls import path
from weddings.views import WeddingsCategoryViewSet, WeddingSubCategoryViewSet
from categories.views import CategoryViewSet
from store.views import StoreViewSet, OfferingViewSet, ReviewViewSet, StoreImageViewSet  # Import the StoreImageViewSet
from users.views import CustomUserViewSet, MessageViewSet, LikeViewSet, CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # Weddings category and subcategory
    path('weddingscategory/', WeddingsCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('weddingscategory/<int:pk>/', WeddingsCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
    path('weddingsubcategory/', WeddingSubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('weddingsubcategory/<int:pk>/', WeddingSubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # Categories
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Store-related URLs
    path('store_list/', StoreViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('store_list/<int:pk>/', StoreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    # Reviews and offerings for a store
    path('store_list/<int:store_id>/reviews/', ReviewViewSet.as_view({'get': 'list_by_store'}), name='reviews_by_store'),
    path('store_list/<int:store_id>/offerings/', OfferingViewSet.as_view({'get': 'list_by_store'}), name='offerings_by_store'),

    # Store images - listing and uploading images
    path('store_list/<int:store_id>/images/', StoreImageViewSet.as_view({'get': 'list_by_store', 'post': 'create'}), name='images_by_store'),
    path('store_list/images/<int:pk>/', StoreImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='image_detail'),
    path('store_list/<int:store_id>/upload-multiple-images/', StoreImageViewSet.as_view({'post': 'upload_multiple'}), name='upload_multiple_images'),

    # User-related URLs
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Messages and likes
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('likes/<int:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Reviews and offerings
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('offerings/', OfferingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('offerings/<int:pk>/', OfferingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]

