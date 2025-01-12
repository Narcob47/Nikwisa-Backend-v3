from rest_framework import serializers
from .models import Store, StoreReview, Reaction, Offering, StoreImage
from users.models import CustomUser
from categories.models import Category
from event_planning.models import EventPlanningCategories


# User Serializer for nested user details in StoreReview
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_image']

# Store Serializer


# class StoreSerializer(serializers.ModelSerializer):
#     owner = serializers.SerializerMethodField()
#     categories = serializers.SerializerMethodField()  # Changed to SerializerMethodField
#     event_planning_categories = serializers.SerializerMethodField()  # Changed to SerializerMethodField

#     class Meta:
#         model = Store
#         fields = '__all__'  # Include all fields by default
#         read_only_fields = ['rating', 'reviews_count', 'is_verified', 'is_responsive']  # Ensure these fields are read-only

#     def create(self, validated_data):
#         owner = self.context['request'].user  # Assuming the owner is the logged-in user
#         validated_data['owner'] = owner  # Set the owner field to the logged-in user

#         # Extract categories and event planning categories from validated data
#         categories_data = validated_data.pop('categories', [])
#         event_planning_categories_data = validated_data.pop('event_planning_categories', [])
        
#         # Create the store instance without categories or event planning categories
#         store = super().create(validated_data)
        
#         # Set the categories and event planning categories
#         store.categories.set(categories_data)
#         store.event_planning_categories.set(event_planning_categories_data)
        
#         store.save()  # Save the store after adding the relationships
#         return store
    
#     def get_owner(self, obj):
#         return obj.owner.username if obj.owner else None

#     def get_categories(self, obj):
#         # Return slugs of categories instead of their primary keys
#         return [category.slug for category in obj.categories.all()]

#     def get_event_planning_categories(self, obj):
#         # Return slugs of event planning categories instead of their primary keys
#         return [event_category.slug for event_category in obj.event_planning_categories.all()]

#     def to_representation(self, instance):
#         # Get the default representation (this includes all fields)
#         data = super().to_representation(instance)
        
#         # Ensure these fields appear in the response
#         data['rating'] = instance.rating
#         data['reviews_count'] = instance.reviews_count
#         data['is_verified'] = instance.is_verified
#         data['is_responsive'] = instance.is_responsive
        
#         return data


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    event_planning_categories = serializers.PrimaryKeyRelatedField(queryset=EventPlanningCategories.objects.all(), many=True)

    class Meta:
        model = Store
        fields = '__all__'  # Include all fields by default
        read_only_fields = ['rating', 'reviews_count', 'is_verified', 'is_responsive']  # Ensure these fields are read-only

    def create(self, validated_data):
        owner = self.context['request'].user  # Assuming the owner is the logged-in user
        validated_data['owner'] = owner  # Set the owner field to the logged-in user

        # Extract categories and event planning categories from validated data
        categories_data = validated_data.pop('categories', [])
        event_planning_categories_data = validated_data.pop('event_planning_categories', [])

        # Create the store instance without categories or event planning categories
        store = super().create(validated_data)

        # Set the categories and event planning categories
        store.categories.set(categories_data)
        store.event_planning_categories.set(event_planning_categories_data)

        store.save()  # Save the store after adding the relationships
        return store

    def get_owner(self, obj):
        return obj.owner.username if obj.owner else None

    def to_representation(self, instance):
        # Get the default representation (this includes all fields)
        data = super().to_representation(instance)

        # Replace category and event planning category IDs with their slugs
        data['categories'] = [category.slug for category in instance.categories.all()]
        data['event_planning_categories'] = [
            epc.slug for epc in instance.event_planning_categories.all()
        ]

        # Ensure these fields appear in the response
        data['rating'] = instance.rating
        data['reviews_count'] = instance.reviews_count
        data['is_verified'] = instance.is_verified
        data['is_responsive'] = instance.is_responsive

        return data


    
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



class StoreImageSerializer(serializers.ModelSerializer):
    # This field will accept a list of images
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )

    class Meta:
        model = StoreImage
        fields = ['id', 'store', 'images', 'uploaded_at']

    def create(self, validated_data):
        images = validated_data.pop('images')
        store = validated_data.get('store')
        
        store_images = []
        for image in images:
            store_image = StoreImage(store=store, image=image)
            store_image.save()
            store_images.append(store_image)

        return store_images

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            data['image'] = request.build_absolute_uri(instance.image.url)
        return data


