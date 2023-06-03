from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserManager
from .serializers import UserRegistrationSerializer

class Register(APIView):
    '''registration to the application'''
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        '''api to create a user'''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
    