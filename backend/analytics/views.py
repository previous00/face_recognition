from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import UserActivity
from .serializers import UserActivitySerializer
from users.permissions import IsAdmin
from papers.models import Paper
from projects.models import ResearchProject


class MyActivityView(generics.ListAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).select_related('content_type')[:100]


class MySummaryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        activities = UserActivity.objects.filter(user=user)
        last_30_days = timezone.now() - timedelta(days=30)
        recent = activities.filter(timestamp__gte=last_30_days)

        summary = {
            'total_papers': Paper.objects.filter(uploaded_by=user).count(),
            'total_projects': user.research_projects.count(),
            'total_favorites': user.favorites.count(),
            'total_views': activities.filter(action='view').count(),
            'total_downloads': activities.filter(action='download').count(),
            'total_searches': activities.filter(action='search').count(),
            'recent_views': recent.filter(action='view').count(),
            'recent_downloads': recent.filter(action='download').count(),
            'recent_searches': recent.filter(action='search').count(),
        }
        return Response(summary)


class PopularPapersView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        papers = Paper.objects.order_by('-view_count')[:10]
        data = [
            {'id': p.id, 'title': p.title, 'authors': p.authors,
             'view_count': p.view_count, 'download_count': p.download_count}
            for p in papers
        ]
        return Response(data)


class TrendingTopicsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_7_days = timezone.now() - timedelta(days=7)
        paper_ct = ContentType.objects.get_for_model(Paper)
        recent_viewed_paper_ids = (
            UserActivity.objects
            .filter(action='view', content_type=paper_ct, timestamp__gte=last_7_days)
            .values_list('object_id', flat=True)
        )
        keywords_raw = (
            Paper.objects
            .filter(id__in=recent_viewed_paper_ids)
            .values_list('keywords', flat=True)
        )
        keyword_count = {}
        for kw_str in keywords_raw:
            if kw_str:
                for kw in kw_str.split(','):
                    kw = kw.strip()
                    if kw:
                        keyword_count[kw] = keyword_count.get(kw, 0) + 1

        trending = sorted(keyword_count.items(), key=lambda x: -x[1])[:20]
        return Response([{'keyword': k, 'count': v} for k, v in trending])


class SystemOverviewView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        last_30_days = timezone.now() - timedelta(days=30)
        data = {
            'total_users': User.objects.count(),
            'active_users_30d': User.objects.filter(last_login__gte=last_30_days).count(),
            'total_papers': Paper.objects.count(),
            'total_projects': ResearchProject.objects.count(),
            'total_activities': UserActivity.objects.count(),
            'activities_30d': UserActivity.objects.filter(timestamp__gte=last_30_days).count(),
            'action_distribution': list(
                UserActivity.objects
                .filter(timestamp__gte=last_30_days)
                .values('action')
                .annotate(count=Count('id'))
                .order_by('-count')
            ),
        }
        return Response(data)


class UserStatsView(views.APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        users = User.objects.annotate(
            activity_count=Count('activities')
        ).order_by('-activity_count')[:20]

        data = [
            {'id': u.id, 'username': u.username, 'activity_count': u.activity_count,
             'last_login': u.last_login}
            for u in users
        ]
        return Response(data)
