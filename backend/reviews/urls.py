from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.ReviewViewSet)

urlpatterns = router.urls + [
    path('<int:review_id>/comments/', views.CommentListCreateView.as_view()),
]
