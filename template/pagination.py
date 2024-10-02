from rest_framework.pagination import PageNumberPagination

class LicensePagination (PageNumberPagination) : 
    page_size = 10