from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

# test password recovery
class PasswordRecoveryTestCase(TestCase):
    def test_password_recover(self):
        # test user
        self.credentials_1 = {
            'username': 'test_user_1',
            'email': 'test_user_1@mail.com',
            'password': 't7t^YmuNGgZXvbpb',
        }

        # create new users
        User.objects.create_user(**self.credentials_1)

        # submit email to password recovery
        # can only test response code as password recovery confirmation page is designed NOT to leak ANY authenticaton information
        #regardless of whether the email lookup is successful, users will be redirected to password recovery confirmation page
        self.response = Client().post('/authentication/recover-password', {'email': 'test_user_1@mail.com'})
        self.assertTrue(self.response.status_code == 302) # responds with 302 redirect

# tests creation of new user via user creation page
class CreateAccountTestCase(TestCase):
    def test_create_account(self):
        # valid credentials
        self.credentials_1 = {
            'username': 'test_user_1',
            'email': 'test_user_1@mail.com',
            'password_1': 't7t^YmuNGgZXvbpb',
            'password_2': 't7t^YmuNGgZXvbpb',
        }

        # invalid credentials - passwords do not match
        self.credentials_2 = {
            'username': 'test_user_2',
            'email': 'test_user_2@mail.com',
            'password_1': 'fpdd53xfqDXH9DFf',
            'password_2': 'fpdd35xfqDXH9DFf',
        }

        # create general_users group
        general_users_group = Group()
        general_users_group.name = 'general_users'
        general_users_group.save()

        # submits new account information
        self.response = Client().post('/authentication/create-account', self.credentials_1)
        self.response = Client().post('/authentication/create-account', self.credentials_2)

        # retrieves newly created account
        new_user_1 = User.objects.get(username=self.credentials_1['username'], email=self.credentials_1['email'])
        try:
            new_user_2 = User.objects.get(username=self.credentials_2['username'], email=self.credentials_1['email'])
        except:
            new_user_2 = None
        
        self.assertTrue(new_user_1) # checks existence of newly created account
        self.assertTrue(new_user_2 == None) # checks if account with invalid information was created
        self.assertTrue(general_users_group.user_set.all().count() == 1) # checks if newly created account was successfully added to general_users group

# creates three new users, logs in user 2, evaluates which users are logged in
class SessionLoginTestCase(TestCase):    
    def test_session_login(self):
        # user 1
        self.credentials_1 = {
        'username': 'test_user_1',
        'password': 'tub3r2xwm&G#^QX3'
        }

        # user 2
        self.credentials_2 = {
        'username': 'test_user_2',
        'password': 'XpRWTcc9e@sqcnKE'
        }

        # user 3
        self.credentials_3 = {
        'username': 'test_user_3',
        'password': 'Aay^4$EAZfP5U2Ty'
        }

        # create new users
        User.objects.create_user(**self.credentials_1)
        User.objects.create_user(**self.credentials_2)
        User.objects.create_user(**self.credentials_3)

        # logs in user 2
        self.response = Client().post('/authentication/session-login', self.credentials_2)
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