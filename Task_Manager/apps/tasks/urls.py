from django.urls import path

from .views import MyTasksListView

app_name = 'apps.tasks'

urlpatterns = [
    path('tasks/', MyTasksListView.as_view(), name='my_tasks'),

]