import django_filters
from .models import Project, Issue


class IssueFilter(django_filters.FilterSet):
    class Meta:
        model = Issue
        fields = ['project']