from rest_framework import serializers
from .models import Favorite
from movies.serializers import MovieListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    movie_detail = MovieListSerializer(source='movie', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'movie_detail', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_movie(self, value):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, movie=value).exists():
            raise serializers.ValidationError('已经收藏过该电影')
        return value
