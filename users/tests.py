import json
import bcrypt
import jwt

from django.test import TestCase, Client
from .models import User
from noticeboard.settings import SECRET_KEY
from my_settings import ALGORITHM


class UserSignupTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_view_post_user_successfully(self):
        client = Client()

        user = {
            'username' : 'test123',
            'email'    : 'test@gmail.com',
            'password' : 'Aaaa123@'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_signup_view_post_invalid_email(self):
        client = Client()

        user = {
            'username': 'test123',
            'email': 'testgmail.com',
            'password': 'Aaaa123@'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_view_post_invalid_password(self):
        client = Client()

        user = {
            'username': 'test123',
            'email': 'test@gmail.com',
            'password': 'Aaaa1'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_signup_view_post_duplicate_email(self):
        client = Client()

        User.objects.create(
            username='setup123',
            email='setup_test@gmail.com',
            password='Aaaa123@'
        )

        user = {
            'username': 'test123',
            'email': 'setup_test@gmail.com',
            'password': 'Aaaa123@'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_view_post_key_error(self):
        client = Client()

        user = {
            'username11111': 'test123',
            'email': 'test@gmail.com',
            'password': 'Aaaa123@'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)


class LoginViewTest(TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw("Aaaa123@".encode('utf-8'), bcrypt.gensalt())
        db_password = hashed_password.decode('utf-8')

        User.objects.create(
            username = 'test123',
            email='test@gmail.com',
            password=db_password
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_login_view_post_user_login_success(self):
        client = Client()

        login_user = {
            'username' : 'test123',
            'password' : 'Aaaa123@'
        }

        user = User.objects.get(username=login_user['username'])

        if User.objects.filter(username=login_user['username']).exists():
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
            response = client.post('/users/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 200)


    def test_login_view_post_user_invalid_username(self):
        client = Client()

        login_user = {
            'username' : 'test123@@@@',
            'password' : 'Aaaa123@'
        }

        if User.objects.filter(username=login_user['username']).exists():
            user = User.objects.get(username=login_user['username'])
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)

        response = client.post('/users/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_login_view_post_user_invalid_password(self):
        client = Client()

        login_user = {
            'username': 'test123',
            'password': 'Aaaa123@@@'
        }

        if User.objects.filter(username=login_user['username']).exists():
            user = User.objects.get(username=login_user['username'])
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)

        response = client.post('/users/login', json.dumps(login_user), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_login_view_post_user_key_error(self):
        client = Client()

        user = {
            'username': 'test123',
            'passworddddddddd': 'Aaaa123@'
        }
        response = client.post('/users/login', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
