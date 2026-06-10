from django.db import models
from django.conf import settings


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='reviews', verbose_name='电影')
    title = models.CharField('标题', max_length=200, blank=True, default='')
    content = models.TextField('内容', blank=True, default='')
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField('发表时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '影评'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['user', 'movie']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', verbose_name='影评')
    content = models.TextField('评论内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    created_at = models.DateTimeField('评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'
