from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserActivity(models.Model):
    ACTION_CHOICES = (
        ('view', '浏览'),
        ('search', '搜索'),
        ('download', '下载'),
        ('favorite', '收藏'),
        ('unfavorite', '取消收藏'),
        ('create', '创建'),
        ('update', '更新'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    metadata = models.JSONField(default=dict, blank=True, help_text='额外数据：搜索关键词、筛选条件等')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activities'
        ordering = ['-timestamp']
        verbose_name = '用户行为'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', 'action', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.timestamp}'
