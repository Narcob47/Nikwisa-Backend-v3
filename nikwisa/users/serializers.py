from rest_framework import serializers
from .models import CustomUser, Message, Like

class CustomUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)  # Add the profile_image field

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'profile_image']  # Include profile_image


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False)  # Optional profile_image field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'profile_image']  # Include profile_image

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data['user_type'],
            profile_image=validated_data.get('profile_image', None)  # Handle profile_image
        )
        return user
