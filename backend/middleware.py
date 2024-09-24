import logging
logger = logging.getLogger('backend')


class GlobalLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Incoming Request: {request.method} {request.path} - Data: {request.body}")

        response = self.get_response(request)

        logger.info(f"Response Status: {response.status_code} - Response Data: {response.content.decode('utf-8')}")

        return response

