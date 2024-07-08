import datetime
import random
import string
from typing import Optional

import redis
from django.conf import settings
from django.utils.safestring import mark_safe
from rest_framework.request import Request

from backend.settings import RedisDatabases
from tep_user import constants as user_const
from tep_user.tasks import send_email

from .redis_pool import RedisPoolStorage


class IPControlService:
    def __init__(self, request: Request, database: RedisDatabases):
        self.request = request
        self.redis_conn = redis.Redis.from_pool(RedisPoolStorage.get_redis_pool(database))

    def __del__(self):
        self.redis_conn.close()

    def _get_ip_address(self):
        x_real_ip = self.request.META.get('HTTP_X_REAL_IP')
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return x_real_ip or (x_forwarded_for and x_forwarded_for.split(',')[0]) or remote_addr

    def check_registration_ip_access(self) -> bool:
        ip_address = self._get_ip_address()
        if settings.DEBUG and not ip_address:
            return True

        if not ip_address:
            return False

        ip_address_access_count = self.redis_conn.get(ip_address) or 0
        if int(ip_address_access_count) == user_const.MAX_REGISTER_IP_COUNT:
            return False

        self.redis_conn.incr(ip_address, 1)
        self.redis_conn.expire(ip_address, datetime.timedelta(hours=1).seconds)

        return True


class INotificationService:
    def verification_code(self, code: str) -> 'INotificationService':
        raise NotImplementedError

    def new_password(self, password: str) -> 'INotificationService':
        raise NotImplementedError

    def login_attempt(self) -> 'INotificationService':
        raise NotImplementedError

    def send(self) -> None:
        raise NotImplementedError


class EmailService(INotificationService):
    def __init__(
            self,
            recipient: str,
            subject: Optional[str] = None,
            body: Optional[str] = None,
            template_name: str = 'index.html',
            context: Optional[dict] = None
    ):
        self.subject = subject
        self.body = body
        self.recipient = recipient
        self.template_name = template_name
        self.context = context or dict()

    def verification_code(self, code: str) -> 'EmailService':
        self.subject = user_const.REGISTRATION_SUBJECT
        self.template_name = 'registration.html'
        self.context['code'] = code
        return self

    def new_password(self, password: str) -> 'EmailService':
        self.subject = user_const.FORGET_PASSWORD_SUBJECT
        self.template_name = 'password.html'
        self.context['password'] = password
        return self
    
    def submit_application(self, full_name: str) -> 'EmailService':
        self.subject = user_const.SUBMIT_APPLICATION_SUBJECT
        self.template_name = 'submit_application.html'
        self.context['full_name'] = full_name
        return self

    def send(self) -> None:
        send_email.delay(
            subject=self.subject,
            template_name=self.template_name,
            recipient_list=[self.recipient],
            context={
                'body': mark_safe(self.body),
                **self.context
            }
        )


class UserService:
    @staticmethod
    def gen_code(email: str) -> str:
        code = str(random.randint(1000, 9999))
        redis_conn = redis.Redis.from_pool(RedisPoolStorage.get_redis_pool(RedisDatabases.LOGIN_CODE))
        redis_conn.set(email, code, datetime.timedelta(minutes=5).seconds)
        return code

    @staticmethod
    def get_code(email: str) -> str:
        redis_conn = redis.Redis.from_pool(RedisPoolStorage.get_redis_pool(RedisDatabases.LOGIN_CODE))
        code = redis_conn.get(email)
        return code and code.decode('utf-8')

    @staticmethod
    def gen_password() -> str:
        characters = [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8)]
        random.shuffle(characters)
        return ''.join(characters)

