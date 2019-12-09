from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from webapp.filteres import IssueFilter
from webapp.models import Project, Issue, Team
from api_v2.serializers import ProjectSerializer, IssueSerializer
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions,\
    DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     else:
    #         return super().get_permissions()


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # filterset_fields = ['project']
    filter_backends = [DjangoFilterBackend]
    filterset_class = IssueFilter


# class TeamViewSet(viewsets.ModelViewSet):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})