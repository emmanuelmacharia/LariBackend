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
        try:
            serializer.save()
        except:
            error_message = "Email or phone number already exists"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyUser(APIView):
    '''verifies a user's email'''
    pass    

