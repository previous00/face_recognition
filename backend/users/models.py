from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
