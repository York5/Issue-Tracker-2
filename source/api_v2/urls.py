from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, IssueViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'issues', IssueViewSet)
# router.register(r'teams', TeamViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]