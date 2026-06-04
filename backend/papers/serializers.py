from rest_framework import serializers
from .models import Paper


class PaperListSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True, default='')

    class Meta:
        model = Paper
        fields = ['id', 'title', 'authors', 'keywords', 'publication_date',
                  'source_journal', 'view_count', 'download_count',
                  'uploaded_by_name', 'created_at']


class PaperDetailSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True, default='')

    class Meta:
        model = Paper
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'view_count', 'download_count', 'created_at', 'updated_at']


class PaperCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ['title', 'authors', 'abstract', 'keywords', 'publication_date',
                  'source_journal', 'doi', 'file']
