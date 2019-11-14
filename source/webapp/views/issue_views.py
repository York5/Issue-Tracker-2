from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from webapp.forms import IssueForm, SimpleSearchForm, ProjectIssueForm
from webapp.models import Issue, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    model = Issue
    ordering = ['-created_at']
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = SimpleSearchForm(data=self.request.GET)
        self.search = None
        if self.form.is_valid():
            self.search_value = self.form.cleaned_data['search']
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_value)
                | Q(description__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_form(self):
        return SimpleSearchForm(data=self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleanned_data['search']
        return None


class IssueView(DetailView):
    template_name = 'issues/issue.html'
    model = Issue


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = IssueForm
    model = Issue
    template_name = 'issues/create.html'
    context_object_name = 'issue_obj'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:issue_view', kwargs={'pk': self.object.pk})


class IssueForProjectCreateView(UserPassesTestMixin, CreateView):
    model = Issue
    template_name = 'issues/create.html'
    form_class = ProjectIssueForm

    def test_func(self):
        project_users = []
        for user in self.get_project().users.all():
            project_users.append(user)
            print(user)
        return self.request.user in project_users

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_project()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.project.issues.create(
            created_by=self.request.user,
            **form.cleaned_data
        )
        return redirect('webapp:project_view', pk=self.project.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'project': self.get_project()})
        return kwargs

    def get_project(self):
        project_pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=project_pk)


class IssueUpdateView(UserPassesTestMixin, UpdateView):
    model = Issue
    template_name = 'issues/update.html'
    form_class = IssueForm
    context_object_name = 'issue'

    def test_func(self):
        project_users = []
        for user in self.get_object().project.users.all():
            project_users.append(user)
        return self.request.user in project_users

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     if hasattr(self, 'object'):
    #         kwargs.update({'project': self.get_project()})
    #     return kwargs
    #
    # def get_project(self):
    #     project_pk = self.kwargs.get('pk')
    #     return get_object_or_404(Project, pk=project_pk)

    def get_success_url(self):
        return reverse('webapp:issue_view', kwargs={'pk': self.object.pk})


class IssueDeleteView(UserPassesTestMixin, DeleteView):
    model = Issue
    template_name = 'issues/delete.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        project_users = []
        for user in self.get_object().project.users.all():
            project_users.append(user)
        return self.request.user in project_users

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


