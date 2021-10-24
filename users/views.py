import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View
from .models import User
from noticeboard.settings import SECRET_KEY
from my_settings import ALGORITHM


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.search('[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+', data['email']) :
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not re.fullmatch('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status = 400)

            User.objects.create(
                username = data['username'],
                email = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
            )

            return JsonResponse({'message' : 'USER CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse(
                        {'message': 'SUCCESS', 'access_token': access_token}, status=200)

                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)