from webapp.models import Project, Issue, User, Team
from rest_framework import serializers


class IssueSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'summary', 'description', 'status', 'type', 'project', 'created_at', 'created_by', 'assigned_to')


# class TeamSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Team
#         fields = ('project', 'user', 'date_started', 'date_finished')


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username')


class ProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    issues = IssueSerializer(many=True, read_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)


    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'status', 'users', 'issues')




