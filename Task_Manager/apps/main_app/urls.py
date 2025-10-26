from django.urls import path

from .views import MyTasksListView, ProjectCreateView, TaskCreateView, UsersListView, UserTasksView, MainView, \
    ProjectDeleteView, ProjectsListView, TaskDeleteView

app_name = 'apps.main_app'

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),

    path('tasks/', MyTasksListView.as_view(), name='my_tasks'),
    path('tasks/create', TaskCreateView.as_view(), name='task_create'),
    path('tasks/delete/<int:pk>', TaskDeleteView.as_view(), name='task_delete'),

    path('projects/', ProjectsListView.as_view(), name='projects_view'),
    path('project/create', ProjectCreateView.as_view(), name='project_create'),
    path('project/delete', ProjectDeleteView.as_view(), name='project_delete'),

    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:user_id>', UserTasksView.as_view(), name='users_tasks')


]