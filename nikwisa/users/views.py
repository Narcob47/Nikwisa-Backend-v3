from django.shortcuts import render
from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, Message, Like, Token, PhoneNumber
from .serializers import CustomUserSerializer, MessageSerializer, LikeSerializer, RegisterSerializer, TokenSerializer, PhoneNumberSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
# from twilio.rest import Client
import random
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from store.models import Store
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email 
        token['user_type'] = user.user_type  
        token['username'] = user.username  # Add the username to the token

        # Retrieve the storeId from the Store model
        try:
            store = Store.objects.get(owner=user)
            token['store_id'] = store.id
            print(f"Store found: {store.name} (ID: {store.id})")
        except Store.DoesNotExist:
            print("No store found for the user.")
            token['store_id'] = None

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Save tokens to the database
        access_token_expiry = now() + timedelta(minutes=5)  # Example access token expiry
        refresh_token_expiry = now() + timedelta(days=1)   # Example refresh token expiry

        Token.objects.update_or_create(
            user=user,
            defaults={
                'access_token': data['access'],
                'refresh_token': data['refresh'],
                'access_token_expires_at': access_token_expiry,
                'refresh_token_expires_at': refresh_token_expiry,
            }
        )

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenSerializer
    
    
    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)

    def get(self, request):
        """
        Fetch the current user's tokens.
        """
        try:
            token = Token.objects.get(user=request.user)
            return Response({
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "access_token_expires_at": token.access_token_expires_at,
                "refresh_token_expires_at": token.refresh_token_expires_at,
            }, status=200)
        except Token.DoesNotExist:
            return Response({"error": "No tokens found for this user."}, status=404)

    def delete(self, request):
        """
        Delete the current user's tokens (logout).
        """
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Tokens deleted successfully."}, status=200)
        except Token.DoesNotExist:
            return Response({"error": "No tokens found for this user."}, status=404)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email', 'user_type']
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def login(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class RegisterView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate OTP
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        user.otp = otp  # Save the OTP in the user's record
        user.is_active = False  # Set the user as inactive until OTP is verified
        user.save()

        # Send OTP via SMS
        self.send_otp(user.phone_number, otp)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully. OTP has been sent.", "user": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def send_otp(self, phone_number, otp):
        if not phone_number:  # Skip sending OTP if phone_number is not provided
            return
        try:
            api_url = "https://gateway.excitesms.com/api/http/sms/send"
            api_token = "60|mfe20oEXTmfhTXiQxM9QYj26NrTGBSmoMDUFg9BQ94ccb932"
            sender_id = "Narco"
            message = f"Your OTP is {otp}. Please use it to verify your account."

            payload = {
                "api_token": "61|phlabtEzEyrVRPV82FqPf2kUsEp4tPLx6puMpWag3c6cc37f",
                "recipient": +260761308936,
                "sender_id": sender_id,
                "type": "otp",
                "message": message
            }

            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

        except requests.exceptions.RequestException as e:
            print(f"Failed to send OTP: {e}")

class VerifyOtpView(viewsets.ViewSet):
    """
    Handle OTP verification, account update, and account deletion.
    """

    @action(detail=False, methods=['post'], url_path='verify-otp', url_name='verify-otp')
    def verify_otp(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return Response(
                {"error": "Phone number and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(phone_number=phone_number, otp=otp)
            ...
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid OTP or phone number."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['put'], url_path='update-account', url_name='update-account')
    def update_account(self, request, *args, **kwargs):
        """
        Update account details for a user.
        """
        phone_number = request.data.get('phone_number')

        try:
            user = CustomUser.objects.get(phone_number=phone_number, is_active=True)
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Account updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found or inactive."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['delete'], url_path='delete-account', url_name='delete-account')
    def delete_account(self, request, *args, **kwargs):
        """
        Delete a user account.
        """
        phone_number = request.data.get('phone_number')

        try:
            user = CustomUser.objects.get(phone_number=phone_number, is_active=True)
            user.delete()
            return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found or inactive."},
                status=status.HTTP_404_NOT_FOUND
            )

class PhoneNumberView(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.save()

        # Generate OTP
        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        # Save the OTP in the phone number record
        phone_number.otp = otp
        phone_number.save()

        # Send OTP via SMS
        self.send_otp(phone_number.phone_number, otp)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Phone number registered successfully. OTP has been sent.", "phone_number": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def send_otp(self, phone_number, otp):
        if not phone_number:  # Skip sending OTP if phone_number is not provided
            return
        try:
            api_url = "https://gateway.excitesms.com/api/v3/sms/send"
            api_token = "61|phlabtEzEyrVRPV82FqPf2kUsEp4tPLx6puMpWag3c6cc37f"
            sender_id = "Narco"
            message = f"Your OTP is {otp}. Please use it to verify your account."

            payload = {
                "api_token": api_token,
                "recipient": phone_number,
                "sender_id": sender_id,
                "type": "otp",
                "message": message
            }

            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

        except requests.exceptions.RequestException as e:
            print(f"Failed to send OTP: {e}")