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


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()  # Custom field to display owner's username
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    event_planning_categories = serializers.PrimaryKeyRelatedField(
        queryset=EventPlanningCategories.objects.all(), many=True
    )
    image = serializers.SerializerMethodField()  # Custom handling for the image field

    class Meta:
        model = Store
        fields = '__all__'  # Include all fields from the model
        read_only_fields = ['rating', 'reviews_count', 'is_verified', 'is_responsive']  # Ensure these fields are read-only

    def get_image(self, obj):
        """Return an absolute URL for the image field."""
        request = self.context.get('request')
        if obj.image:
            # Build an absolute URL if request context is available
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_owner(self, obj):
        """Return the username of the owner."""
        return obj.owner.username if obj.owner else None

    def create(self, validated_data):
        """Override create to handle many-to-many relationships."""
        owner = self.context['request'].user  # The logged-in user is the owner
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

    def update(self, instance, validated_data):
        """Override update to handle many-to-many relationships."""
        # Extract categories and event planning categories from validated data
        categories_data = validated_data.pop('categories', None)
        event_planning_categories_data = validated_data.pop('event_planning_categories', None)

        # Update the instance with the remaining data
        instance = super().update(instance, validated_data)

        # Update categories and event planning categories if provided
        if categories_data is not None:
            instance.categories.set(categories_data)
        if event_planning_categories_data is not None:
            instance.event_planning_categories.set(event_planning_categories_data)

        instance.save()  # Save the store after adding the relationships
        return instance

    def to_representation(self, instance):
        """Customize the representation of the serialized data."""
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

        # Include image as an absolute URL
        data['image'] = self.get_image(instance)

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
    # Accepts a list of images when used with bulk uploads
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = StoreImage
        fields = ['id', 'store', 'image', 'images', 'uploaded_at']

    def create(self, validated_data):
        """
        Handles creation of single or multiple StoreImage instances.
        """
        images = validated_data.pop('images', None)  # Extract 'images' from data
        store = validated_data.get('store')

        # Single Image Upload
        if not images:
            return super().create(validated_data)

        # Bulk Image Upload
        store_images = [StoreImage(store=store, image=image) for image in images]
        StoreImage.objects.bulk_create(store_images)  # Save all at once

        return store_images

    def to_representation(self, instance):
        """
        Modify representation for bulk uploads.
        """
        if isinstance(instance, list):
            return [self.single_instance_representation(img) for img in instance]
        return self.single_instance_representation(instance)

    def single_instance_representation(self, instance):
        """
        Helper method to serialize a single StoreImage instance.
        """
        data = {
            'id': instance.id,
            'store': instance.store.id,
            'image': self.context['request'].build_absolute_uri(instance.image.url),  # Builds the full URL for the image
            'uploaded_at': instance.uploaded_at,
        }
        return data

