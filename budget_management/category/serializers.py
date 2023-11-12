from rest_framework import serializers

from budget_management.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "category_name", "is_status")
