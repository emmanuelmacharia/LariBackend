from django.http import HttpResponseServerError


class ExceptionHandlerMiddleware:
    '''global exception handler for the project'''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = HttpResponseServerError("Something went wrong")
        return response