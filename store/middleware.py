from django.utils.deprecation import MiddlewareMixin


class SaveIpAddressMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')

        ip = x_real_ip or (x_forwarded_for and x_forwarded_for.split(',')[0]) or remote_addr
        request.ip_address = ip
