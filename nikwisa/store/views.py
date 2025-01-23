from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, StoreReview, Reaction, Offering, StoreImage
from rest_framework.decorators import action
from .serializers import StoreSerializer, StoreReviewSerializer, ReactionSerializer, OfferingSerializer, StoreImageSerializer
import logging
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StoreViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create, update, or delete stores

    def list(self, request):
        """
        Fetch all stores for everyone (authenticated or unauthenticated users)
        """
        stores = Store.objects.all()  # Fetch all stores for everyone
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a store (only for authenticated users)
        """
        # Pass the request context to the serializer
        serializer = StoreSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()  # The logged-in user will be set as owner in the serializer
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Fetch a specific store by ID for everyone
        """
        store = Store.objects.filter(pk=pk).first()
        if not store:
            raise NotFound(detail="Store not found.")
        
        serializer = StoreSerializer(store)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update an existing store (only for authenticated users)
        """
        store = Store.objects.filter(pk=pk).first()
        if not store:
            raise NotFound(detail="Store not found.")

        serializer = StoreSerializer(store, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Partially update an existing store (only for authenticated users)
        """
        store = Store.objects.filter(pk=pk).first()
        if not store:
            raise NotFound(detail="Store not found.")

        serializer = StoreSerializer(store, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Delete a store (only for authenticated users)
        """
        store = Store.objects.filter(pk=pk).first()
        if not store:
            raise NotFound(detail="Store not found.")
        
        store.delete()
        return Response({'detail': 'Store deleted successfully.'}, status=204)

    @action(detail=False, methods=['get'], url_path='by_user')
    def list_by_user(self, request):
        """
        Fetch only the stores created by the authenticated user
        This endpoint is for use in the dashboard for managing/editing stores
        """
        stores = Store.objects.filter(owner=request.user)  # Filter by the logged-in user's ID
        serializer = StoreSerializer(stores, many=True, context={'request': request})
        return Response(serializer.data)




class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = StoreReview.objects.all()
        serializer = StoreReviewSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreReviewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        review = get_object_or_404(StoreReview, pk=pk)
        serializer = StoreReviewSerializer(review, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        review = get_object_or_404(StoreReview, pk=pk)
        serializer = StoreReviewSerializer(review, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        review = get_object_or_404(StoreReview, pk=pk)
        review.delete()
        return Response({'detail': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk=None):
        """
        Handle partial updates for StoreReview.
        """
        review = get_object_or_404(StoreReview, pk=pk)
        serializer = StoreReviewSerializer(review, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Handle full updates for StoreReview.
        """
        review = get_object_or_404(StoreReview, pk=pk)
        serializer = StoreReviewSerializer(review, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='store_list/(?P<store_id>\d+)/reviews', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        store = get_object_or_404(Store, id=store_id)
        reviews = StoreReview.objects.filter(store=store)
        serializer = StoreReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
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

class StoreImageViewSet(viewsets.ModelViewSet):
    queryset = StoreImage.objects.all()
    serializer_class = StoreImageSerializer

    # Action to upload multiple images
    @action(detail=True, methods=['post'], url_path='upload-multiple-images', url_name='upload_multiple_images')
    def upload_multiple(self, request, store_id=None):
        """
        Upload multiple images for a specific store in one request.
        """
        store_id = store_id  # Use the store_id passed as part of the URL
        images = request.FILES.getlist('images')  # Get multiple files from the request

        if not store_id:
            return Response({'detail': 'Store ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not images:
            return Response({'detail': 'No images were provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store = Store.objects.get(id=store_id)  # Verify the store exists
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Save each image
        store_images = []
        for image in images:
            store_images.append(StoreImage(store=store, image=image))

        StoreImage.objects.bulk_create(store_images)  # Save all images in one operation

        return Response({'detail': f'{len(store_images)} images uploaded successfully.'}, status=status.HTTP_201_CREATED)

    # Action to fetch all images for a specific store
    @action(detail=True, methods=['get'], url_path='images', url_name='store_images')
    def list_by_store(self, request, store_id=None):
        """
        Fetch all images for a specific store.
        """
        try:
            store = Store.objects.get(id=store_id)  # Fetch the store based on the store_id in the URL
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

        store_images = StoreImage.objects.filter(store=store)  # Fetch all images related to this store
        # Now serialize them into an array of image URLs
        serializer = StoreImageSerializer(store_images, many=True, context={'request': request})  # Pass the request context here
        # Modify the representation to return just URLs in an array
        image_urls = [request.build_absolute_uri(image['image']) for image in serializer.data]

        return Response({
            'id': store.id,
            'name': store.name,
            'images': image_urls  # Return images as an array of URLs
        }, status=status.HTTP_200_OK)
