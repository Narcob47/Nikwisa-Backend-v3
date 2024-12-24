from rest_framework import serializers
from .models import Store, StoreReview, Reaction, Offering

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class StoreRviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

class OfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering
        fields = ['name', 'description', 'image', 'price', 'store', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']