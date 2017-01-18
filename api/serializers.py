from rest_framework import serializers

from ..models import CategoryPage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPage

        # Add category_page (nested relation) with live (field)
        # this to render a hyperlink to page on the (client)filter node-item
        fields = ('id', 'title', 'depth', 'url')
