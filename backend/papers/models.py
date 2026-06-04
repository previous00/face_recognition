from django.db import models
from django.conf import settings


class Paper(models.Model):
    title = models.CharField(max_length=500, verbose_name='标题')
    authors = models.TextField(verbose_name='作者', help_text='多个作者用逗号分隔')
    abstract = models.TextField(blank=True, verbose_name='摘要')
    keywords = models.CharField(max_length=500, blank=True, verbose_name='关键词', help_text='多个关键词用逗号分隔')
    publication_date = models.DateField(null=True, blank=True, verbose_name='发表日期')
    source_journal = models.CharField(max_length=300, blank=True, verbose_name='来源期刊')
    doi = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='DOI')
    file = models.FileField(upload_to='papers/%Y/%m/', null=True, blank=True, verbose_name='文件')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='uploaded_papers', verbose_name='上传者'
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    download_count = models.PositiveIntegerField(default=0, verbose_name='下载次数')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'papers'
        ordering = ['-created_at']
        verbose_name = '论文'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
