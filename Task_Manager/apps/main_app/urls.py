from django.urls import path

from .views import MyTasksListView, ProjectCreateView, TaskCreateView, UsersListView, UserTasksView

app_name = 'apps.main_app'

urlpatterns = [
    path('tasks/', MyTasksListView.as_view(), name='my_tasks'),
    path('tasks/create', TaskCreateView.as_view(), name='task_create'),
    path('project/create', ProjectCreateView.as_view(), name='project_create'),

    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:user_id>', UserTasksView.as_view(), name='users_tasks')


]