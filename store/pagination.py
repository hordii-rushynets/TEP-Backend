from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    max_page_size = 1000

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')

        if page_size is None:
            return None

        try:
            page_size = int(page_size)
        except ValueError:
            return None

        return page_size if page_size > 0 else None

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)

        if page_size is None:
            return None

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

