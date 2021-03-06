from django import forms
from django.contrib.auth.models import User

from webapp.models import Status, Type, Issue, Project, Team


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['created_at', 'created_by']

    # def __init__(self, project, *args, **kwargs):
    #     super(IssueForm, self).__init__(*args, **kwargs)
    #     self.fields['assigned_to'].queryset = User.objects.filter(projects=project)


class ProjectIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ['created_at', 'project', 'created_by']

    def __init__(self, project, *args, **kwargs):
        super(ProjectIssueForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(projects=project)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['type_name']


class ProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
                       widget=forms.CheckboxSelectMultiple,
                       queryset=User.objects.all(),
                    )

    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at']

    def __init__(self, user_id, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['users'].initial = User.objects.get(id=user_id)


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = []