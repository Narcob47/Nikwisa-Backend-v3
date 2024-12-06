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

    def validate_date(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Date must be a string in the format YYYY-MM-DD")
        return value