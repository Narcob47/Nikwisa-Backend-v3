from rest_framework import serializers
from .models import CustomUser, Message, Like, Token, PhoneNumber

class CustomUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)  # Add the profile_image field

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'profile_image']  # Include profile_image
        
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['access_token', 'refresh_token', 'access_token_expires_at', 'refresh_token_expires_at']


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
        phone_number = validated_data.get('phone_number', None)
        if not phone_number:
            validated_data['phone_number'] = None  # Explicitly set to None if not provided
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data['user_type'],
            profile_image=validated_data.get('profile_image', None),
            phone_number=validated_data.get('phone_number', None),  # Include phone_number
        )
        return user
    
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']

class UserTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_type']
