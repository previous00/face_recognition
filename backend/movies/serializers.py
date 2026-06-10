from rest_framework import serializers
from .models import Category, Movie


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    favorites_count = serializers.IntegerField(source='favorites.count', read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster', 'director', 'release_date', 'rating',
                  'rating_count', 'category', 'category_name', 'favorites_count', 'reviews_count']


class MovieDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    favorites_count = serializers.IntegerField(source='favorites.count', read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['created_by', 'created_at', 'rating', 'rating_count']
