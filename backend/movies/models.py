from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField('分类名称', max_length=50, unique=True)
    description = models.TextField('描述', blank=True)

    class Meta:
        verbose_name = '电影分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField('片名', max_length=200)
    description = models.TextField('剧情简介')
    poster = models.ImageField('海报', upload_to='posters/', blank=True)
    director = models.CharField('导演', max_length=100)
    actors = models.CharField('主演', max_length=500)
    release_date = models.DateField('上映日期')
    duration = models.IntegerField('片长(分钟)')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    rating = models.DecimalField('评分', max_digits=2, decimal_places=1, default=0)
    rating_count = models.IntegerField('评分人数', default=0)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_rating(self):
        """根据所有影评评分重新计算平均分"""
        result = self.reviews.aggregate(avg=Avg('rating'), count=models.Count('id'))
        self.rating = round(result['avg'], 1) if result['avg'] else 0
        self.rating_count = result['count']
        self.save(update_fields=['rating', 'rating_count'])
