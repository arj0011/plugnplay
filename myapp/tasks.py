from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_registration_email(self, to_email, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task
def send_campaign_email():
    User = get_user_model()
    emails = list(User.objects.values_list('email', flat=True))
    
    if not emails:
        return "No users found."

    send_mail(
        subject="🚀 New Features from PlugnPlay!",
        message="We're excited to share new updates with you...",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False
    )
    return f"Sent campaign email to {len(emails)} users."