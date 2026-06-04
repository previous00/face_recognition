from rest_framework import serializers
from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'username', 'action', 'content_type_name', 'object_id',
                  'metadata', 'ip_address', 'timestamp']

    def get_content_type_name(self, obj):
        if obj.content_type:
            return obj.content_type.model
        return None
