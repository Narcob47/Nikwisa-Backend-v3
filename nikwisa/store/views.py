from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, StoreReview, Reaction, Offering, StoreImage
from rest_framework.decorators import action
from .serializers import StoreSerializer, StoreReviewSerializer, ReactionSerializer, OfferingSerializer, StoreImageSerializer
import logging

logger = logging.getLogger(__name__)

class StoreViewSet(viewsets.ViewSet):
    def list(self, request):
        logger.info(f"Owner data: {request.data.get('owner')}")
        queryset = Store.objects.all()
        serializer = StoreSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store, context={'request': request})
        return Response([serializer.data])

    def update(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        store.delete()
        return Response({'detail': 'Store deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = StoreReview.objects.all()
        serializer = StoreReviewSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreReviewSerializer(review, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreReviewSerializer(review, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='store_list/(?P<store_id>\d+)/reviews', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        try:
            store = Store.objects.get(id=store_id)
            reviews = StoreReview.objects.filter(store=store)
            serializer = StoreReviewSerializer(reviews, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)


class LikeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Reaction.objects.all()
        serializer = ReactionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ReactionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response({'detail': 'Reaction not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionSerializer(like, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response({'detail': 'Reaction not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionSerializer(like, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response({'detail': 'Reaction not found.'}, status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response({'detail': 'Reaction deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class OfferingViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Offering.objects.all()
        serializer = OfferingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = OfferingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response({'detail': 'Offering not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response({'detail': 'Offering not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response({'detail': 'Offering not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response({'detail': 'Offering not found.'}, status=status.HTTP_404_NOT_FOUND)
        offering.delete()
        return Response({'detail': 'Offering deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='store/(?P<store_id>\d+)/offerings', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        try:
            store = Store.objects.get(id=store_id)
            offerings = Offering.objects.filter(store=store)
            serializer = OfferingSerializer(offerings, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)



# StoreImageViewSet (New ViewSet)
class StoreImageViewSet(viewsets.ModelViewSet):
    queryset = StoreImage.objects.all()
    serializer_class = StoreImageSerializer
 # Custom action to handle bulk image upload
    @action(detail=True, methods=['post'], url_path='upload-multiple-images', url_name='upload_multiple')
    def upload_multiple(self, request, pk=None):
        """
        Upload multiple images for a specific store.
        """
        # Retrieve store ID from URL parameters (pk)
        store = self.get_object()  # Automatically gets the store object using pk (primary key)

        # Get images from the request (multiple files)
        files = request.FILES.getlist('images')  # This will retrieve all files uploaded under 'images' key
        
        if not files:
            return Response({'detail': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create StoreImage instances for each uploaded file
        images = []
        for file in files:
            image_instance = StoreImage.objects.create(store=store, image=file)
            images.append(image_instance)

        # Serialize and return the uploaded images
        serializer = StoreImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        List all store images.
        """
        queryset = StoreImage.objects.all()
        serializer = StoreImageSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new store image.
        """
        serializer = StoreImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific store image by ID.
        """
        try:
            store_image = StoreImage.objects.get(pk=pk)
        except StoreImage.DoesNotExist:
            return Response({'detail': 'Store image not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StoreImageSerializer(store_image, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update an existing store image.
        """
        try:
            store_image = StoreImage.objects.get(pk=pk)
        except StoreImage.DoesNotExist:
            return Response({'detail': 'Store image not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StoreImageSerializer(store_image, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Partially update a store image (e.g., updating description).
        """
        try:
            store_image = StoreImage.objects.get(pk=pk)
        except StoreImage.DoesNotExist:
            return Response({'detail': 'Store image not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StoreImageSerializer(store_image, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a store image.
        """
        try:
            store_image = StoreImage.objects.get(pk=pk)
        except StoreImage.DoesNotExist:
            return Response({'detail': 'Store image not found.'}, status=status.HTTP_404_NOT_FOUND)
        store_image.delete()
        return Response({'detail': 'Store image deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='store/(?P<store_id>\d+)/images', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        """
        List all images for a specific store.
        """
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        store_images = StoreImage.objects.filter(store__id=store_id)
        serializer = StoreImageSerializer(store_images, many=True, context={'request': request})
        return Response(serializer.data)




# from django.shortcuts import render
# from rest_framework import viewsets, filters, status
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Store, StoreReview, Reaction, Offering
# from rest_framework.decorators import action
# from .serializers import StoreSerializer, StoreReviewSerializer, ReactionSerializer, OfferingSerializer
# import logging
# logger = logging.getLogger(__name__)

# class StoreViewSet(viewsets.ViewSet):
#     def list(self, request):
#         logger.info(f"Owner data: {request.data.get('owner')}")
#         queryset = Store.objects.all()
#         serializer = StoreSerializer(queryset, many=True, context={'request': request})  # Pass context
#         return Response(serializer.data)


#     def create(self, request):
#         """
#         Create a new store.
#         """
#         serializer = StoreSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StoreSerializer(store, context={'request': request})
#         return Response([serializer.data])

#     def update(self, request, pk=None):
#         """
#         Update a store by replacing all fields.
#         """
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = StoreSerializer(store, data=request.data, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         """
#         Partially update a store (only fields provided in the request).
#         """
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = StoreSerializer(store, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         """
#         Delete a store.
#         """
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

#         store.delete()
#         return Response({'detail': 'Store deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

# class ReviewViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StoreReview.objects.all()
#         serializer = StoreReviewSerializer(queryset, many=True, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StoreReviewSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreReviewSerializer(review, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreReviewSerializer(review, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(detail=False, methods=['get'], url_path='store_list/(?P<store_id>\d+)/reviews', url_name='list_by_store')
#     def list_by_store(self, request, store_id=None):
#         try:
#             store = Store.objects.get(id=store_id)
#             reviews = StoreReview.objects.filter(store=store)
#             serializer = StoreReviewSerializer(reviews, many=True, context={'request': request})  # Pass context
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)


# class LikeViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Reaction.objects.all()
#         serializer = ReactionSerializer(queryset, many=True, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReactionSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ReactionSerializer(like, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ReactionSerializer(like, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         like.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class OfferingViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Offering.objects.all()
#         serializer = OfferingSerializer(queryset, many=True, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = OfferingSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, context={'request': request})  # Pass context
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def partial_update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data, partial=True, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         offering.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(detail=False, methods=['get'], url_path='store/(?P<store_id>\d+)/offerings', url_name='list_by_store')
#     def list_by_store(self, request, store_id=None):
#         try:
#             store = Store.objects.get(id=store_id)
#             offerings = Offering.objects.filter(store=store)
#             serializer = OfferingSerializer(offerings, many=True, context={'request': request})  # Pass context
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND) 


# from django.shortcuts import render
# from rest_framework import viewsets, filters, status
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Store, StoreReview, Reaction, Offering
# from rest_framework.decorators import action
# from .serializers import StoreSerializer, StoreReviewSerializer, ReactionSerializer, OfferingSerializer

# class StoreViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Store.objects.all()
#         serializer = StoreSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StoreSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreSerializer(store)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreSerializer(store, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             store = Store.objects.get(pk=pk)
#         except Store.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         store.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StoreReview.objects.all()
#         serializer = StoreReviewSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StoreReviewSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreReviewSerializer(review)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = StoreReviewSerializer(review, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             review = StoreReview.objects.get(pk=pk)
#         except StoreReview.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(detail=False, methods=['get'], url_path='store_list/(?P<store_id>\d+)/reviews', url_name='list_by_store')
#     def list_by_store(self, request, store_id=None):
#         try:
#             store = Store.objects.get(id=store_id)
#             reviews = StoreReview.objects.filter(store=store)
#             serializer = StoreReviewSerializer(reviews, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)


# class LikeViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Reaction.objects.all()
#         serializer = ReactionSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReactionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ReactionSerializer(like)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ReactionSerializer(like, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, pk=None):
#         try:
#             like = Reaction.objects.get(pk=pk)
#         except Reaction.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         like.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class OfferingViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Offering.objects.all()
#         serializer = OfferingSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context
    
#     def create(self, request):
#         serializer = OfferingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         offering.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#     @action(detail=False, methods=['get'], url_path='store/(?P<store_id>\d+)/offerings', url_name='list_by_store')
#     def list_by_store(self, request, store_id=None):
#         try:
#             store = Store.objects.get(id=store_id)
#             offerings = Offering.objects.filter(store=store)

#             # Debug: Check if offerings is a queryset (it should be)
#             print("Offerings Queryset:", offerings)

#             # Serialize the queryset directly as 'many=True'
#             serializer = OfferingSerializer(offerings, many=True)

#             # Debug: Check the serialized data before returning
#             print("Serialized Offerings:", serializer.data)

#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Store.DoesNotExist:
#             return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)






# class OfferingViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Offering.objects.all()
#         serializer = OfferingSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = OfferingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = OfferingSerializer(offering, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         try:
#             offering = Offering.objects.get(pk=pk)
#         except Offering.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         offering.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
# Create your views here.