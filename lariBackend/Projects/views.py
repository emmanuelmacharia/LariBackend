from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProjectsSerializers
from core.helpers.auth_token_decorator import auth_token_validator

class CreateViewProject(APIView):
    '''create and read all api view'''
    serializer_class = ProjectsSerializers

    @auth_token_validator
    def post(self, request, format=None):
        '''creates a new project'''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except:
            error_message = "Sorry, we cant complete this request at the moment, please try again"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        # TODO: add a try except block to create a record in project partners; you should already have request.user, and the project id
        return Response(serializer.data, status=status.HTTP_201_CREATED)


