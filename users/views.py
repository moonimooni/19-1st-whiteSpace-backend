import re
import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .utils       import email_validator, password_validator, phone_validator
from my_settings  import ALGORITHM, SECRET

from .models      import User


class SignUpView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            email          = data['email']
            password       = data['password']
            password_check = data['password_check']
            name           = data['name']
            phone_number   = data['phone_number']

            if not email_validator(email):
                return JsonResponse({'MESSAGE' : 'INVALID EMAIL'}, status=400)

            if not password_validator(password):
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'}, status=400)
            
            if not phone_validator(phone_number):
                return JsonResponse({'MESSAGE' : 'INVALID PHONE NUMBER'}, status=400)

            if password != password_check:                
                return JsonResponse({'MESSAGE' : 'PASSWORD NOT MATCH'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    
            User.objects.create(
                email        = email,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
                is_active    = True,
                mileage      = 0
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)
            
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE' : 'WRONG PASSWORD'}, status=401)

            access_token = jwt.encode({'user_id' : user.id}, SECRET, ALGORITHM)
            
            return JsonResponse({'MESSAGE' : 'SUCCESS' , 'access_token' : access_token}, status=200)
            
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

class CheckEmailView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            email = data['email']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL ALREADY EXISTS'}, status=400)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)
