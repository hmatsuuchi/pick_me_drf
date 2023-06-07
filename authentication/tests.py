from django.test import TestCase, Client
from django.contrib.auth.models import User

# creates three new users, logs in user 2, evaluates which users are logged in
class SessionLoginTestCase(TestCase):
    def create_users(self):
        # user 1
        self.credentials_1 = {
        'username': 'test_user_01',
        'password': 'tub3r2xwm&G#^QX3'
        }
        # user 2
        self.credentials_2 = {
        'username': 'test_user_02',
        'password': 'XpRWTcc9e@sqcnKE'
        }
        # user 3
        self.credentials_3 = {
        'username': 'test_user_03',
        'password': 'Aay^4$EAZfP5U2Ty'
        }
        User.objects.create_user(**self.credentials_1)
        User.objects.create_user(**self.credentials_2)
        User.objects.create_user(**self.credentials_3)
        
    def test_session_login(self):
        self.create_users()

        # logs in user 2
        self.response = Client().post('/authentication/session-authenticate', self.credentials_2)
        logged_in_user = self.response.wsgi_request.user

        # checks login status of user 1; should be false
        user_1 = User.objects.get(username=self.credentials_1['username'])
        self.assertFalse(user_1 == logged_in_user)
        # checks login status of user 2; should be true
        user_2 = User.objects.get(username=self.credentials_2['username'])
        self.assertTrue(user_2 == logged_in_user)
        # checks login status of user 3; should be false
        user_3 = User.objects.get(username=self.credentials_3['username'])
        self.assertFalse(user_3 == logged_in_user)