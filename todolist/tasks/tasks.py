from celery import shared_task
from django.utils import timezone
from .models import Task



@shared_task
def notify_task_due():
    # Получаем текущее время
    now = timezone.now()

    # Фильтруем задачи, у которых дата совпадает с текущей датой, час и минута равны текущим, и которые не завершены
    due_tasks = Task.objects.filter(
    due_date__date=now.date(),
    due_date__hour=now.hour,
    due_date__minute=now.minute,
    completed=False
).select_related('user', 'category')
    
    for task in due_tasks:
        # Логика отправки уведомления (например, email или другой способ)
        print(f"Задача {task.title} должна быть выполнена сейчас пользователем {task.user.username}")
