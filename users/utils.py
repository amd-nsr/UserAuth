from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None and response.data:
        response.data['status_code'] = response.status_code
        response.data ={"errors" : response.data}
    return response