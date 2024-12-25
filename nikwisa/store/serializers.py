from rest_framework import serializers
from .models import Store, StoreReview, Reaction, Offering
from users.models import CustomUser
from categories.models import Category
from weddings.models import WeddingsCategory

# User Serializer for nested user details in StoreReview
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_image']

# Store Serializer
class StoreSerializer(serializers.ModelSerializer):
    # Fetch the owner's username instead of the owner ID
    owner = serializers.SerializerMethodField()
    # Fetch category titles instead of category IDs
    categories = serializers.SerializerMethodField()
    # Fetch wedding category title instead of wedding category ID
    wedding_category = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = '__all__'  # Keep all other fields as they are

    def get_owner(self, obj):
        return obj.owner.username if obj.owner else None

    def get_categories(self, obj):
        return [category.title for category in obj.categories.all()]

    def get_wedding_category(self, obj):
        return obj.wedding_category.title if obj.wedding_category else None

# StoreReview Serializer with nested user details
class StoreReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include nested user data

    class Meta:
        model = StoreReview
        fields = ['id', 'rating', 'comment', 'created_at', 'store', 'user']

# Reaction Serializer
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

# Offering Serializer
class OfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering
        fields = [
            'id', 'name', 'description', 'image', 'price', 
            'store', 'phone_number', 'whatsapp_number', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = float(instance.price)  # Convert Decimal to float
        return data
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None




# from rest_framework import serializers
# from .models import Store, StoreReview, Reaction, Offering
# from users.models import CustomUser
# from categories.models import Category
# from weddings.models import WeddingsCategory

# class StoreSerializer(serializers.ModelSerializer):
#     # Fetch the owner's username instead of the owner ID
#     owner = serializers.SerializerMethodField()
#     # Fetch category titles instead of category IDs
#     categories = serializers.SerializerMethodField()
#     # Fetch wedding category title instead of wedding category ID
#     wedding_category = serializers.SerializerMethodField()

#     class Meta:
#         model = Store
#         fields = '__all__'  # Keep all other fields as they are

#     def get_owner(self, obj):
#         return obj.owner.username if obj.owner else None

#     def get_categories(self, obj):
#         return [category.title for category in obj.categories.all()]

#     def get_wedding_category(self, obj):
#         return obj.wedding_category.title if obj.wedding_category else None

# class StoreReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreReview
#         fields = '__all__'

# class ReactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reaction
#         fields = '__all__'

# class OfferingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offering
#         fields = ['name', 'description', 'image', 'price', 'store', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']


# from rest_framework import serializers
# from .models import Store, StoreReview, Reaction, Offering

# class StoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Store
#         fields = '__all__'

# class StoreRviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreReview
#         fields = '__all__'

# class ReactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reaction
#         fields = '__all__'

# class OfferingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offering
#         fields = ['name', 'description', 'image', 'price', 'store', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']