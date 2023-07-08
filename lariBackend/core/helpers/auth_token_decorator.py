import jwt
from functools import wraps
from django.conf import settings
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response



def auth_token_validator(f):
    '''decorator to verify the auth token passed from client'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        '''validates the token'''
        user = ''
        user_token = ''

        for arg in args:
            if not isinstance(arg, Request):
                continue
            user = arg.user
            user_token = arg.headers.get('Authorization').split(' ')[1]
            break
        
        try:
            jwt_payload = jwt.decode(
                user_token,
                settings.SECRET_KEY,
                algorithms=settings.SIMPLE_JWT['ALGORITHM'],
                audience=settings.SIMPLE_JWT['AUDIENCE'], 
                issuer=settings.SIMPLE_JWT['ISSUER'],
                verify=True)
            if jwt_payload['user_id'] != user.userId:
                return  Response({'successful': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return  Response({'successful': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return  Response({'successful': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidAudienceError:
            return  Response({'successful': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    return wrapper
