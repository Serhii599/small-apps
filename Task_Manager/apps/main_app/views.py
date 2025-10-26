from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

from .forms import TaskCreationForm, ProjectCreationForm
from .models import *

User = get_user_model()


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main_app:my_tasks')
        else:
            return redirect('authentication:login')


class MyTasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main_app/my_task_list.html'

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class OneTaskListView(LoginRequiredMixin, ListView):
    pass

class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'main_app/projects_list.html'


class OneProjectListView(LoginRequiredMixin, ListView):
    pass

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = "main_app/project_create.html"
    success_url = reverse_lazy("main_app:project_create")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


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
    model = Task
    success_url = reverse_lazy('main_app:my_tasks')

class UsersListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'main_app/users_list.html'

class UserTasksView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main_app/user_tasks.html'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assignee_id=user_id).select_related('assignee')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']

        # спробуємо отримати користувача без try/except через get_object_or_404:
        context['user'] = get_object_or_404(User, id=user_id)

        return context