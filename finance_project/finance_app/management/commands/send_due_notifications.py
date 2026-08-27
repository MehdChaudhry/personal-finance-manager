import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from finance_app.models import Task

class Command(BaseCommand):
    help = 'Notify users about tasks that are near their due date'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        notification_time = now + datetime.timedelta(hours=24)  # Notify 24 hours before due date
        tasks_due_soon = Task.objects.filter(due_date__lte=notification_time, due_date__gt=now)

        for task in tasks_due_soon:
            # Notify the user (you can customize how to notify the user)
            send_mail(
                subject="Task Due Soon",
                message=f"Your task '{task.description}' is due on {task.due_date}.",
                from_email="admin@taskapp.com",
                recipient_list=[task.user.email],
            )
            self.stdout.write(self.style.SUCCESS(f"Notified about task: {task.description}"))

