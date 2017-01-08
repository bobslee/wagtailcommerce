from rest_framework import serializers

from ..models import CategoryPage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPage
        fields = ('id', 'title', 'depth', 'url')
