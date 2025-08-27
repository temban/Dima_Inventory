from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', 'An error occurred'),
                'details': response.data
            }
        }
        response.data = custom_response
    
    return response

class InsufficientStockException(Exception):
    pass

def handle_insufficient_stock_exception(exc, context):
    response = Response(
        {
            'error': {
                'code': 400,
                'message': 'Insufficient stock for this operation',
                'details': str(exc)
            }
        },
        status=status.HTTP_400_BAD_REQUEST
    )
    return response