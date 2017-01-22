from rest_framework import serializers

from ..models import Category, CategoryPage

from wagtailcommerce.utils.text import chunk_string_increment

class CategoryPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPage
        fields = ('id', 'title', 'live', 'full_url')
        
class CategorySerializer(serializers.ModelSerializer):
    category_page = CategoryPageSerializer(read_only=True)
    ancestor_paths = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'path', 'ancestor_paths', 'title', 'depth', 'category_page')

    def get_ancestor_paths(self, obj):
        paths = chunk_string_increment(obj.path, Category.steplen)
        return paths[0:-1]
