from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from webapp.forms import ProjectForm, SimpleSearchForm
from webapp.models import Project, STATUS_CHOICES, Team
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ProjectIndexView(ListView):
    template_name = 'projects/project_index.html'
    context_object_name = 'projects'
    model = Project
    ordering = ['-created_at']
    paginate_by = 6
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
                Q(name__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
    #   context['active_project'] = self.model.objects.filter(status='active').order_by('created_at')
    #   context['closed_project'] = self.model.objects.filter(status='closed').order_by('created_at')
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class ProjectView(PermissionRequiredMixin, DetailView):
    template_name = 'projects/project.html'
    model = Project
    permission_required = 'webapp.project_view'
    permission_denied_message = '403 Access Denied!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        issues = project.issues.order_by('-created_at')
        paginator = Paginator(issues, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        teams = Team.objects.filter(project=self.get_project()).select_related()
        context['teams'] = teams
        context['paginator'] = paginator
        context['page_obj'] = page
        context['issues'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        return context

    def get_project(self):
        project_pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=project_pk)


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    model = Project
    template_name = 'projects/project_create.html'
    permission_required = 'webapp.project_add'
    permission_denied_message = '403 Access Denied!'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     if hasattr(self, 'object'):
    #         kwargs.update({'user': self.request.user})
    #     return kwargs


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'webapp.project_update'
    permission_denied_message = '403 Access Denied!'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('webapp:project_index')
    permission_required = 'webapp.project_delete'
    permission_denied_message = '403 Access Denied!'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = 'closed'
        self.object.save()
        return HttpResponseRedirect(success_url)
