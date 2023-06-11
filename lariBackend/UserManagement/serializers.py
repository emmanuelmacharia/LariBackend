from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from core.cache_management.cache_management import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''serializer for the registration api - creates a new user'''
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            "min_length": "Password must be at least 8 characters long",
            "max_length": "Password is too long"
        }
    )

    confirmed_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            "min_length": "Password must be at least 8 characters long",
            "max_length": "Password is too long"
        }
    )

    class Meta:
        '''meta class for the user serializer'''
        model = User
        fields = [
            'userId',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'confirmed_password']

    def validate(self, data):
        ''' validates the registration request'''
        try:
            validate_password(data['password'])
        except ValidationError as error:
            raise serializers.ValidationError(
                {
                    "passoword":
                    str(error).replace("[" ", " ").replace(" "]", "")
                }
            )

        if not self.passwords_match(data):
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        del validated_data["confirmed_password"]
        return User.objects.create_user(**validated_data)

    def passwords_match(self, data) -> bool:
        '''checks if the passwords match'''
        password1 = data.get('password')
        password2 = data.get('confirmed_password')
        return password1 == password2


class UserVerificationSerializer(serializers.ModelSerializer):
    '''Email verification serializer class'''
    class Meta:
        model = User
        fields = ['userId', 'token']

    def create_verification_token(self, data):
        '''creates the verification token and adds it to the cache'''
        # avoid creating two tokens from the same user; instead, check whether the user already has a valid token in cache
        pass

    def retreive_verification_token(self) -> str:
        '''fetches the verification token from the db'''
        verification_cache_response = get_data_from_cache('verification_token')
        verification_token = ''

        if not verification_cache_response:
            return 'Could not retrieve data from cache'

        if verification_cache_response['successful']:
            verification_token = verification_cache_response['response']

        return verification_token

    def verify_tokens(self, data) -> bool:
        '''verifies the tokens sent for email verification'''
        usertoken = data.get('token')
        createdtoken = self.retreive_verification_token()

        return usertoken == createdtoken

    def validate(self, data):
        if not data['userId']:
            return
        if not data['token']:
            return
        return data

    def update(self, instance, validated_data):
        if not self.verify_tokens(validated_data):
            return
        instance.user_verified = True
        instance.save()
        return instance

class LoginSerializer(TokenObtainPairSerializer):
    '''custom serializer class for login and token generation'''

    class Meta:
        model = User

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom parameters to the token payload
        token['userId'] = user.userId

        return token


    def get_user(self, email):
        user = ''
        try:
            user =  User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        return user
    
    def check_for_email_verification(self, user) -> bool:
        #TODO: verify that the user trying to log in has their email verified
        print(user.user_verified)
        return True

    def validate(self, attrs):
        # import pdb; pdb.set_trace()
        # is_verified = self.check_for_email_verification(self.user)
        user_email = attrs['email']
        user =self.get_user(user_email)
        is_verified = True

        if not is_verified:
            #TODO: send the user a magic link to their email; create verification api  
            pass

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access']= str(refresh.access_token)
        return data