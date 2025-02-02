from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from .models import User, StoredJWT, Message, Like, Review
from .serializers import MessageSerializer, LikeSerializer, ReviewSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Store JWT in DB
        StoredJWT.objects.update_or_create(
            user=user,
            defaults={'access_token': access_token, 'refresh_token': refresh_token}
        )

        return Response({"access": access_token, "refresh": refresh_token})
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        StoredJWT.objects.filter(user=user).delete()  # Remove stored JWTs
        logout(request)
        return Response({"message": "Logged out successfully"})

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        stored_jwt = StoredJWT.objects.filter(user=user).first()
        
        if not stored_jwt:
            return Response({"error": "No valid refresh token found"}, status=400)
        
        try:
            refresh = RefreshToken(stored_jwt.refresh_token)
            access_token = str(refresh.access_token)
            
            # Update stored access token
            stored_jwt.access_token = access_token
            stored_jwt.save()

            return Response({"access": access_token})
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=400)


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

# Like ViewSet
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)