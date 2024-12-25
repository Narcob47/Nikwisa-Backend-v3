from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, StoreReview, Reaction, Offering
from rest_framework.decorators import action
from .serializers import StoreSerializer, StoreReviewSerializer, ReactionSerializer, OfferingSerializer

class StoreViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Store.objects.all()
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = StoreReview.objects.all()
        serializer = StoreReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StoreReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StoreReviewSerializer(review)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StoreReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            review = StoreReview.objects.get(pk=pk)
        except StoreReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='store_list/(?P<store_id>\d+)/reviews', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        try:
            store = Store.objects.get(id=store_id)
            reviews = StoreReview.objects.filter(store=store)
            serializer = StoreReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)


class LikeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Reaction.objects.all()
        serializer = ReactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionSerializer(like)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionSerializer(like, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            like = Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OfferingViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Offering.objects.all()
        serializer = OfferingSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def create(self, request):
        serializer = OfferingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OfferingSerializer(offering, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            offering = Offering.objects.get(pk=pk)
        except Offering.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        offering.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['get'], url_path='store/(?P<store_id>\d+)/offerings', url_name='list_by_store')
    def list_by_store(self, request, store_id=None):
        try:
            store = Store.objects.get(id=store_id)
            offerings = Offering.objects.filter(store=store)

            # Debug: Check if offerings is a queryset (it should be)
            print("Offerings Queryset:", offerings)

            # Serialize the queryset directly as 'many=True'
            serializer = OfferingSerializer(offerings, many=True)

            # Debug: Check the serialized data before returning
            print("Serialized Offerings:", serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Store.DoesNotExist:
            return Response({'detail': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

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