import re
import jwt
import json
import bcrypt

from django.http.response import JsonResponse
from my_settings  import SECRET, ALGORITHM
from users.models import User

def password_validator(password):
    validator = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*_-])(\S){8,16}$')
    return validator.match(password)

def email_validator(email):
    validator = re.compile('^[a-zA-Z0-9+-_]+@[a-z]+.[a-z]+')
    return validator.match(email)

def phone_validator(phone):
    validator = re.compile('^\d{9,11}$')
    return validator.match(phone)

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            if not access_token:
                return JsonResponse({'MESSAGE' : 'UNAUTHORIZED ACCESS'}, status=401)

            payload = jwt.decode(access_token, SECRET, ALGORITHM)

            if not User.objects.filter(id=payload['user_id'].exists():
                return JsonResponse({'MESSAGE' : 'USER NOT FOUND'}, status=404)

            request.user = User.objects.get(id=payload['user_id'])
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID TOKEN'}, status=400)
    return wrapper
