import os

from storages.backends.s3boto3 import S3Boto3Storage

SERVER_DOMAIN = os.getenv('SERVER_DOMAIN', 'localhost:8000')


class StaticS3Boto3Storage(S3Boto3Storage):
    location = 'static'


class MediaS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    custom_domain = f'{SERVER_DOMAIN}/media'
