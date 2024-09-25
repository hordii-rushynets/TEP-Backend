import datetime
import os
import random
import string
from typing import Optional
import requests

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
        x_real_ip = self.request.META.get('HTTP_REAL_IP')
        x_forwarded_for = self.request.META.get('HTTP_FORWARDED_FOR')
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return x_real_ip or (x_forwarded_for and x_forwarded_for.split(',')[0]) or remote_addr

    def get_ip(self):
        return self._get_ip_address()

    def _check_ip_access(self, key: str, max_count: int, expire_seconds: int) -> bool:
        ip_address = self._get_ip_address()
        if settings.DEBUG and not ip_address:
            return True

        if not ip_address:
            return False

        ip_address_access_count = self.redis_conn.get(key) or 0
        if int(ip_address_access_count) >= max_count:
            return False

        self.redis_conn.setex(key, expire_seconds, 1)

        return True

    def check_registration_ip_access(self) -> bool:
        ip_address = self._get_ip_address()
        expire_seconds = datetime.timedelta(hours=1).seconds

        return self._check_ip_access(ip_address, user_const.MAX_REGISTER_IP_COUNT, expire_seconds)

    def check_product_number_of_views_ip_access(self, product_slug: str) -> bool:
        ip_address = self._get_ip_address()
        key = f"{ip_address}_product_{product_slug}_views"
        expire_seconds = int(datetime.timedelta(days=7).total_seconds())

        return self._check_ip_access(key, 1, expire_seconds)
    
    def check_product_set_favorite_ip_access(self, product_slug: str) -> bool:
        ip_address = self._get_ip_address()
        key = f"{ip_address}_product_{product_slug}_set_favorite"

        expire_seconds = int(datetime.timedelta(minutes=1).total_seconds())

        return self._check_ip_access(key, user_const.MAX_SET_FAVORITE_PRODUCT_BY_USER, expire_seconds)


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


class MetaPixelService:
    def __init__(self):
        self.__pixel_id = settings.META_PIXEL_ID
        self.__pixel_access_token = settings.META_PIXEL_ACCESS_TOKEN
        self.__api_version = settings.META_GRAPH_API
        self.__url = f"https://graph.facebook.com/{self.__api_version}/{self.__pixel_id}/events?access_token={self.__pixel_access_token}"

    def send(self, event_name: str, event_time: int, event_source_url: str, client_ip_address: str, client_user_agent: str,
             fbc: str, fbp: str, phone: str | None, email: str | None, firstname: str | None, lastname: str | None,
             birthday: str | None, city: str | None, index: str | None, custom_data: dict) -> int:
        body = {
            "data": [
                {
                    "event_name": event_name,
                    "event_time": event_time,
                    "action_source": "website",
                    "event_source_url": event_source_url,
                    "user_data": {
                        "client_ip_address": client_ip_address,
                        "client_user_agent": client_user_agent,
                        "fbc": fbc,
                        "fbp": fbp,


                        "ph": phone,
                        "em": email,
                        "fn": firstname,
                        "ln": lastname,
                        "db": birthday,
                        "ct": city,
                        "zp": index
                    },
                    "custom_data": custom_data,
                }
            ]
        }

        request = requests.post(self.__url, body)
        return request.status_code
