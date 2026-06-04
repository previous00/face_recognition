from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ResearchProject

User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'institution']


class ProjectListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, default='')
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = ResearchProject
        fields = ['id', 'title', 'principal_investigator', 'funding_source',
                  'status', 'start_date', 'end_date', 'view_count',
                  'member_count', 'created_by_name', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, default='')
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchProject
        fields = '__all__'
        read_only_fields = ['created_by', 'view_count', 'created_at', 'updated_at']


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchProject
        fields = ['title', 'principal_investigator', 'description', 'funding_source',
                  'budget', 'status', 'start_date', 'end_date']

    def validate(self, attrs):
        start_date = attrs.get('start_date') or (self.instance and self.instance.start_date)
        end_date = attrs.get('end_date') or (self.instance and self.instance.end_date)
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({'end_date': '结束时间不能早于开始时间'})
        return attrs
