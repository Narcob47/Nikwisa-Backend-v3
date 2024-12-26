from django.urls import path
from weddings.views import WeddingsCategoryViewSet, WeddingSubCategoryViewSet
from categories.views import CategoryViewSet
from store.views import StoreViewSet, OfferingViewSet, ReviewViewSet
from users.views import CustomUserViewSet, MessageViewSet, LikeViewSet, CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        'token/', CustomTokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/', TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    path(
        'register/', RegisterView.as_view(), 
        name='register'
    ), 
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
        'store_list/', StoreViewSet.as_view({
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
    path(
        'store_list/<int:store_id>/reviews/', ReviewViewSet.as_view({
            'get': 'list_by_store'
        }),
        name='reviews_by_store'
    ),
       path(
        'store_list/<int:store_id>/offerings/', OfferingViewSet.as_view({
            'get': 'list_by_store',  # Use the custom action to fetch offerings by store_id
        }),
        name='offerings_by_store'
    ),
    path('users/', CustomUserViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('users/<int:pk>/', CustomUserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('messages/<int:pk>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('likes/', LikeViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('likes/<int:pk>/', LikeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path(
        'reviews/', ReviewViewSet.as_view({
            'get': 'list', 
            'post': 'create'
        })
    ),
    path(
        'reviews/<int:pk>/', ReviewViewSet.as_view({
            'put': 'update', 
            'delete': 'destroy'
        })
    ),
    path(
        'offerings/', OfferingViewSet.as_view({
            'get': 'list', 
            'post': 'create'
        })
    ),
    path(
        'offerings/<int:pk>/', OfferingViewSet.as_view({
            'get': 'retrieve', 
            'put': 'update', 
            'patch': 'partial_update', 
            'delete': 'destroy'
        })
    ),
]


# from django.urls import path
# from weddings.views import WeddingsCategoryViewSet, WeddingSubCategoryViewSet
# from categories.views import CategoryViewSet
# from store.views import StoreViewSet, OfferingViewSet
# from users.views import CustomUserViewSet, MessageViewSet, LikeViewSet, CustomTokenObtainPairView, RegisterView
# from rest_framework_simplejwt.views import TokenRefreshView
# from store.views import ReviewViewSet

# urlpatterns = [
#     path(
#         'token/', CustomTokenObtainPairView.as_view(), 
#         name='token_obtain_pair'
#         ),
#     path(
#         'token/refresh/', TokenRefreshView.as_view(), 
#         name='token_refresh'
#         ),
#     path(
#         'register/', RegisterView.as_view(), 
#         name='register'
#         ), 
#     path(
#         'weddingscategory/', WeddingsCategoryViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         })
#     ),
#     path(
#         'weddingscategory/<int:pk>/', WeddingsCategoryViewSet.as_view({
#             'get': 'retrieve',
#             'put': 'partial_update',
#             'delete': 'destroy',
#         })
#     ),
#     path(
#         'weddingsubcategory/', WeddingSubCategoryViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         })
#     ),
#     path(
#         'weddingsubcategory/<int:pk>/', WeddingSubCategoryViewSet.as_view({
#             'get': 'retrieve',
#             'put': 'partial_update',
#             'delete': 'destroy',
#         })
#     ),
#     path(
#         'categories/', CategoryViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         })
#     ),
#     path(
#         'categories/<int:pk>/', CategoryViewSet.as_view({
#             'get': 'retrieve',
#             'put': 'update',
#             'delete': 'destroy',
#         })
#     ),

#     path (
#         'store_list/', StoreViewSet.as_view({
#         'get': 'list',
#         'post': 'create'
#         })
#     ),

#     path(
#         'store_list/<int:pk>/', StoreViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'patch': 'partial_update',
#         'delete': 'destroy'
#         })
#     ),
#     path('users/', CustomUserViewSet.as_view({
#         'get': 'list',
#         'post': 'create',
#     })),
#     path('users/<int:pk>/', CustomUserViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'delete': 'destroy',
#     })),
#     path('messages/', MessageViewSet.as_view({
#         'get': 'list',
#         'post': 'create',
#     })),
#     path('messages/<int:pk>/', MessageViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'delete': 'destroy',
#     })),
#     path('likes/', LikeViewSet.as_view({
#         'get': 'list',
#         'post': 'create',
#     })),
#     path('likes/<int:pk>/', LikeViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'delete': 'destroy',
#     })),
#     path(
#         'reviews/', ReviewViewSet.as_view({
#             'get': 'list', 
#             'post': 'create'
#         })),
#     path(
#         'reviews/<int:pk>/', ReviewViewSet.as_view({
#             'put': 'update', 
#             'delete': 'destroy'
#     })),
#     path(
#         'offerings/', OfferingViewSet.as_view({
#             'get': 'list', 
#             'post': 'create'
#         })),
#     path(
#         'offerings/<int:pk>/', OfferingViewSet.as_view({
#             'get': 'retrieve', 
#             'put': 'update', 
#             'patch': 'partial_update', 
#             'delete': 'destroy'
#         })),
# ]