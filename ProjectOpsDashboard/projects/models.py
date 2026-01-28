from django.db import models
from django.conf import settings
from core import constants

User = settings.AUTH_USER_MODEL

# ==========================
# ======== PROJECTS ========
# ==========================

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=constants.PROJECT_STATUS, default='pending')
    reason = models.TextField(blank=True, null=True)    # Reason for blocked/rejected.

    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,      # Allows the deletion of the user while retaining the project in the database.
        blank=True,
        null=True,
        related_name='created_projects' # To access all the projects created by the user.
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def completion_percentage(self):
        tasks = self.tasks.filter(parent__isnull=True)

        if not tasks.exists():
            return 0
        
        total = tasks.count()
        completed = sum(1 for task in tasks if task.is_completed())
        return int((completed / total) * 100)

# ======================
# ======= TASKS ========
# ======================

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
        null=True,
        blank=True
    )

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=constants.TASK_STATUS, default='pending')
    priority = models.CharField(max_length=20, choices=constants.TASK_PRIORITY, default='none')

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subtasks',
        on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Deleting a user should not delete the task.
        blank=True,
        null=True,
        related_name='created_tasks'
    )

    class Meta:
        ordering = ['-priority', 'end_date']
    
    def __str__(self):
        return self.title
    
    def is_completed(self):
        if self.subtasks.exists():
            return all(
                subtask.is_completed()
                for subtask in self.subtasks.all()
            )
        
        return self.status == 'finished'
    
    def completion_percentage(self):
        subtasks = self.subtasks.all()

        if not subtasks.exists():
            return 100 if self.status == 'finished' else 0

        total = subtasks.count()
        completed = sum(1 for t in subtasks if t.is_completed())

        return int((completed / total) * 100)