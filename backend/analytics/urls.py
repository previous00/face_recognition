from django.urls import path
from .views import (
    MyActivityView, MySummaryView, PopularPapersView,
    TrendingTopicsView, SystemOverviewView, UserStatsView
)

urlpatterns = [
    path('my-activity/', MyActivityView.as_view(), name='my-activity'),
    path('my-summary/', MySummaryView.as_view(), name='my-summary'),
    path('popular-papers/', PopularPapersView.as_view(), name='popular-papers'),
    path('trending-topics/', TrendingTopicsView.as_view(), name='trending-topics'),
    path('system-overview/', SystemOverviewView.as_view(), name='system-overview'),
    path('user-stats/', UserStatsView.as_view(), name='user-stats'),
]
