from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from django.conf import settings

from .models import UserManager
from .serializers import UserRegistrationSerializer, LoginSerializer

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


class CustomTokenObtainPairView(TokenObtainPairView):
    '''Custom access token generation class'''
    permission_classes = [AllowAny]  # Allow anyone to obtain a token
    serializer_class = LoginSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        expiry = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        expiry /= timedelta(seconds=1)
        modified_data = {
            'access_token': response.data['access'],
            'refresh_token': response.data['refresh'],
            'expires_in':expiry,
            'token_type': 'Bearer',
            'message': 'success',
            'successful': True,
        }

        response.data = modified_data
        return super().finalize_response(request, response, *args, **kwargs)
    


class CustomTokenRefreshView(TokenRefreshView):
    '''Custom refresh token generation class'''
    permission_classes = [AllowAny]  # Allow anyone to refresh a token