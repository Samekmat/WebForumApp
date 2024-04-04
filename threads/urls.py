from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ThreadViewSet, ThreadPostListCreateAPIView

app_name = 'threads'

router = DefaultRouter()
router.register(r'thread', ThreadViewSet, basename='thread')

urlpatterns = [
    path('thread/post/', ThreadPostListCreateAPIView.as_view(), name='thread_posts'),
]

urlpatterns += router.urls
