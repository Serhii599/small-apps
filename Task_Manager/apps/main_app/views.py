from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView

from .forms import TaskCreationForm
from .models import *

class MyTasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main_app/my_task_list.html'

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class OneTaskListView(LoginRequiredMixin, ListView):
    pass

class ProjectsListView(LoginRequiredMixin, ListView):
    pass

class OneProjectListView(LoginRequiredMixin, ListView):
    pass

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_name', 'project_description', 'priority']
    template_name = "main_app/task_create.html"
    success_url = reverse_lazy("main_app:project_create")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "main_app/task_create.html"
    success_url = reverse_lazy("main_app:task_create")

    def form_valid(self, form):
        # приклад, якщо треба підв’язати користувача
        form.instance.creator = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    pass

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    pass

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    pass

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    pass