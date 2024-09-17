from django.db import models
from django.contrib.auth import get_user_model
import hashlib
from django.utils import timezone

User = get_user_model()


def generate_custom_id():
    current_time = str(timezone.now())
    return hashlib.sha256(current_time.encode('utf-8')).hexdigest()


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=64, default=generate_custom_id, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=64, default=generate_custom_id, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(default=timezone.now)  # дата создания задачи
    due_date = models.DateTimeField(blank=True, null=True)   # дедлайн задачи

    def __str__(self):
        return self.title
