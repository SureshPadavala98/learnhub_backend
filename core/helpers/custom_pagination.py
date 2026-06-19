from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'next_page': self.get_next_link(),
            'prev_page': self.get_previous_link(),
            'count': self.page.paginator.count,
            'rows_per_page':self.get_page_size(self.request),
            'results': data
            # **data
        })