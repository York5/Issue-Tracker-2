from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, IssueViewSet, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'issues', IssueViewSet)
# router.register(r'teams', TeamViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('logout/', LogoutView.as_view(), name='delete_auth_token'),
]