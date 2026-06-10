from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.FavoriteViewSet, basename='favorite')

urlpatterns = router.urls
