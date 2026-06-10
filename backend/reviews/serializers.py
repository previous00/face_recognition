from rest_framework import serializers
from .models import Review, Comment
from users.serializers import UserBriefSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['user']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent', 'review']
        read_only_fields = ['id']


class ReviewListSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'movie_title', 'title', 'rating', 'comments_count', 'created_at']


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'movie_title', 'title', 'content', 'rating', 'comments', 'created_at', 'updated_at']

    def get_comments(self, obj):
        top_comments = obj.comments.filter(parent=None)
        return CommentSerializer(top_comments, many=True).data


class ReviewCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True, default='')
    content = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = Review
        fields = ['id', 'movie', 'title', 'content', 'rating']
        read_only_fields = ['id']
