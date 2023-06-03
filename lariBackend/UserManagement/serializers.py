from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserManager


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''serializer for the registration api - creates a new user'''
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(
        max_length=128,
        min_length = 8,
        write_only=True,
        error_messages={
            "min_length": "Password must be at least 8 characters long",
            "max_length": "Password is too long"
        }
    )

    confirmed_password = serializers.CharField(
        max_length=128,
        min_length = 8,
        write_only=True,
        error_messages={
            "min_length": "Password must be at least 8 characters long",
            "max_length": "Password is too long"
        }
    )

    class Meta:
        '''meta class for the user serializer'''
        model = UserManager
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
        del validated_data["confirm_password"]
        return UserManager.objects.create_user(**validated_data)

    def passwords_match(self, data) -> bool:
        '''checks if the passwords match'''
        password1 = data.get['password']
        password2 = data.get['confirmed_password']
        return password1 == password2