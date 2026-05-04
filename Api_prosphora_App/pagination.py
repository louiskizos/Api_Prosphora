from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class BaseCustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class Pagination_payement_offrande(BaseCustomPagination):
    page_size = 200

class Pagination_ahadi(BaseCustomPagination):
    page_size = 400

class Pagination_etat_besoin(BaseCustomPagination):
    page_size = 100


class Pagination_livre_caisse(BaseCustomPagination):
    page_size = 380