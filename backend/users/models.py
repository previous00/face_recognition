from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', '超级管理员'),
        ('admin', '管理员'),
        ('user', '普通用户'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    institution = models.CharField(max_length=200, blank=True, verbose_name='所属机构')
    research_field = models.CharField(max_length=200, blank=True, verbose_name='研究方向')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
