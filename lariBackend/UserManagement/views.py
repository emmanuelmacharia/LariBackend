from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegistrationSerializer, LoginSerializer, UserVerificationSerializer
from .models import User
from django.utils import timezone

class Register(APIView):
    '''registration to the application'''
    serializer_class = UserRegistrationSerializer

    # registration_param_config = openapi.Parameter()
    @swagger_auto_schema(operational_description="creating a user")
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
        user = User.objects.get(email=user_data['email'])
        user_verification = UserVerificationSerializer()
        user_verification.create_verification_token(user, request)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyUser(APIView):
    '''verifies a user's email'''
    serializer_class = UserVerificationSerializer

    def get(self, request): 
        '''responsible for getting a new email sent to the client'''
        token = request.GET.get('token')
        serializer = self.serializer_class(data={'token': token})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        verified_token = self.serializer_class().verify_tokens(data)

        if not verified_token['successful']:
            return Response(verified_token, status=status.HTTP_400_BAD_REQUEST)

        user = verified_token['user']
        if not user.user_verified:
            user.user_verified = True
            user.date_verified = timezone.now()
            user.save()

        return Response({'successful': True, 'message': 'Profile activated'})


    def post(self, request):
        pass

    def put(self, request):
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