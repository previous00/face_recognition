from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Favorite
from papers.serializers import PaperListSerializer
from projects.serializers import ProjectListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    content_object_data = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'content_type', 'object_id', 'content_type_name', 'content_object_data', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_content_type_name(self, obj):
        return obj.content_type.model

    def get_content_object_data(self, obj):
        if obj.content_type.model == 'paper':
            return PaperListSerializer(obj.content_object).data
        elif obj.content_type.model == 'researchproject':
            return ProjectListSerializer(obj.content_object).data
        return None


class FavoriteCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['paper', 'project'])
    object_id = serializers.IntegerField()

    def validate(self, attrs):
        type_map = {
            'paper': 'paper',
            'project': 'researchproject',
        }
        model_name = type_map[attrs['type']]
        try:
            ct = ContentType.objects.get(model=model_name)
            model_class = ct.model_class()
            model_class.objects.get(pk=attrs['object_id'])
        except (ContentType.DoesNotExist, model_class.DoesNotExist):
            raise serializers.ValidationError('目标对象不存在')
        attrs['content_type'] = ct
        return attrs
