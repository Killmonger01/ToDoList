from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')

app = Celery('todolist')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Добавляем планировщик Beat
app.conf.beat_schedule = {
    'check-overdue-tasks-every-minute': {
        'task': 'tasks.tasks.notify_task_due',
        'schedule': 60.0,  # Запускать задачу каждую минуту
    },
}
