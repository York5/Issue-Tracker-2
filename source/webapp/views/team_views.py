from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import TeamForm
from webapp.models import Team


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = 'projects/team_update.html'
    form_class = TeamForm
    context_object_name = 'team'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})