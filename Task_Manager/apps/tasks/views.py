from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView

from .models import *

class MyTasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/my_task_list.html'

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class OneTaskListView(LoginRequiredMixin, ListView):
    pass

class ProjectsListView(LoginRequiredMixin, ListView):
    pass

class OneProjectListView(LoginRequiredMixin, ListView):
    pass

class ProjectCreateView(LoginRequiredMixin, CreateView):
    pass

class TaskCreateView(LoginRequiredMixin, CreateView):
    pass

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    pass

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    pass

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    pass

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    pass