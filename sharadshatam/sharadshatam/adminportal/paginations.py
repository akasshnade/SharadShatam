from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework import status

from rest_framework.exceptions import NotFound  
from rest_framework.exceptions import APIException

class NotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('bad_request.')
    default_code = 'bad_request'


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        
        # try:
        #     if self.page.paginator.count>0:
        #         pn = 1 if not self.page_query_param or self.page_query_param == None else self.page_query_param  

        #         # pn=(self.page_query_param,1)
        #         self.page = self.page.paginator.page(pn)
        # except Exception as exc:
        #     # Here it is
        #     print(exc)
        #     msg = {
        #         "responseCode": 400, # you can remove this line as now the status code will be 400 by default as we have override it in `NotFound` class(see above)
        #         "responseMessage": "Page out of range"
        #     }
        #     raise NotFound(msg)
        response={}
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        response['responseCode'] = 200
        response['responseMessage'] = "Success"
        response['responseData'] = data
        return Response(response,status=status.HTTP_200_OK)
