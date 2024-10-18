from tep_user.services import IPControlService, RedisDatabases
from rest_framework.request import Request


def get_auth_date(request: Request) -> str:
    """
    If user is not authenticated return ip else return user email

    :param request (Request): Request with data
    :return: string
    """

    if request.user.is_authenticated:
        return request.user.email
    else:
        ip_service = IPControlService(request, RedisDatabases.IP_CONTROL)
        return ip_service.get_ip()

