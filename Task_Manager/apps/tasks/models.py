from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class TasksInfo(models.Model):
    class Status(models.TextChoices):
        BACKLOG = 'Backlog'
        TO_DO = 'To do'
        IN_PROGRESS = 'In progress'
        DONE = 'Done'
    class Priorities(models.TextChoices):
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'
        URGENT = 'Urgent'

    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.BACKLOG)
    priority = models.CharField(max_length=100, choices=Priorities.choices, default=None)
    due_date = models.DateTimeField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="tasks")

    created_at = models.DateTimeField()

class Projects(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    project_tasks = models.ManyToManyField(TasksInfo)

