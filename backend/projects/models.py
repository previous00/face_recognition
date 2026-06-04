from django.db import models
from django.conf import settings


class ResearchProject(models.Model):
    STATUS_CHOICES = (
        ('planning', '规划中'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('suspended', '已暂停'),
    )
    title = models.CharField(max_length=500, verbose_name='项目名称')
    principal_investigator = models.CharField(max_length=200, verbose_name='项目负责人')
    description = models.TextField(blank=True, verbose_name='项目描述')
    funding_source = models.CharField(max_length=300, blank=True, verbose_name='资助来源')
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='经费(万元)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name='状态')
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='结束日期')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='research_projects',
        blank=True, verbose_name='项目成员'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_projects', verbose_name='创建者'
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'research_projects'
        ordering = ['-created_at']
        verbose_name = '科研项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
