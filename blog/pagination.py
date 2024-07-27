from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 17
    page_size_query_param = 'page_size'  # Allows you to change the page size through the request parameters
    max_page_size = 100
