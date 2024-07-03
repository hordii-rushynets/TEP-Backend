from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_email(
        subject: str,
        template_name: str,
        recipient_list: list,
        context: dict = None
) -> None:
    context = context or {}
    email = EmailMessage(
        subject=subject,
        body=render_to_string(template_name=template_name, context=context),
        to=recipient_list
    )
    email.content_subtype = 'html'
    email.send()
