from rest_framework import serializers
from .models import WeddingsCategory, WeddingSubCategory, Weddings

class WeddingsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingsCategory
        fields = '__all__'

class WeddingSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingSubCategory
        fields = '__all__'

class WeddingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weddings
        fields = '__all__'