from celery import shared_task
from django.core.mail import send_mail
import os


@shared_task
def send_otp_email_task(email, otp):
    send_mail(
        'OTP for Registration',
        f'Your OTP for registration is: {otp}',
        os.environ.get('EMAIL_LOGIN'),
        [email],
        fail_silently=False,
    )