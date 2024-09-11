from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_marketing as MailchimpMarketing
from django.conf import settings


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


class MailchimpService:
    def __init__(self):
        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_DATA_CENTER
        })

    def subscribe_user(self, email, first_name, last_name):
        try:
            response = self.client.lists.add_list_member(settings.MAILCHIMP_AUDIENCE_ID, {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": first_name,
                    "LNAME": last_name
                }
            })
            return response
        except ApiClientError as error:
            print(f"An error occurred: {error.text}")
            return None


@shared_task
def subscribe_to_mail_chimp(email: str, first_name: str, last_name: str):
    mailchimp_service = MailchimpService()
    mailchimp_service.subscribe_user(email, first_name, last_name)
