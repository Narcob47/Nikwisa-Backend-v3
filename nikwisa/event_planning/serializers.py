from rest_framework import serializers
from .models import EventPlanningSubCategory, EventPlanningCategories

class EventPlanningCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlanningCategories
        fields = '__all__'

class EventPlanningSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlanningSubCategory
        fields = '__all__'

