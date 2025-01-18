from django.shortcuts import render
from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, Message, Like
from .serializers import CustomUserSerializer, MessageSerializer, LikeSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from twilio.rest import Client
import random

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email  # Add email to the token
        token['user_type'] = user.user_type  # Add user_type to the token

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = f"Your OTP is {otp}. Please use it to verify your account."
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
        except Exception as e:
            raise Exception(f"Failed to send OTP: {str(e)}")



    # def send_otp(self, phone_number, otp):
    #     try:
    #         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #         message = f"Your OTP is {otp}. Please use it to verify your account."

    #         client.messages.create(
    #             body=message,
    #             from_=settings.TWILIO_PHONE_NUMBER,
    #             to=phone_number
    #         )
    #     except Exception as e:
    #         raise Exception(f"Failed to send OTP: {str(e)}")


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
    # @action(detail=False, methods=['post'], url_path='verify-otp', url_name='verify-otp')
    # def verify_otp(self, request, *args, **kwargs):
    #     """
    #     Verify the OTP for a given phone number.
    #     """
    #     phone_number = request.data.get('phone_number')
    #     otp = request.data.get('otp')

    #     if not phone_number or not otp:
    #         return Response(
    #             {"error": "Phone number and OTP are required."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:
    #         user = CustomUser.objects.get(phone_number=phone_number, otp=otp)
    #         if not user.is_active:
    #             user.is_active = True  # Activate user account after verification
    #             user.otp = None  # Clear the OTP
    #             user.save()
    #             return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"message": "User is already active."}, status=status.HTTP_200_OK)
    #     except CustomUser.DoesNotExist:
    #         return Response(
    #             {"error": "Invalid OTP or phone number."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

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