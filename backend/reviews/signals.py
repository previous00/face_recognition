from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def update_movie_rating_on_save(sender, instance, **kwargs):
    """影评创建或更新后，重新计算电影平均评分"""
    instance.movie.update_rating()


@receiver(post_delete, sender=Review)
def update_movie_rating_on_delete(sender, instance, **kwargs):
    """影评删除后，重新计算电影平均评分"""
    instance.movie.update_rating()
