from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
# serializers
from authentication.serializers import UserSerializer
# models
from user_profile.models import UserProfile
from django.contrib.auth.models import Group, User
# email
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .tokens import account_activation_token, password_reset_token
from django.contrib.auth import get_user_model

class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class AccountCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Django default User creation
            user = serializer.save()
            # add user to 'general_users' group
            group = Group.objects.get(name='general_users')
            group.user_set.add(user)
            # user extended profile creation
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()

            if user:
                # generate confirmation email
                current_site = get_current_site(self.request)
                send_mail(
                    subject='Verify your account',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    message = render_to_string('authentication/email_verification.html', {
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }),
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountVerify(APIView):
    def post(self, request, uidb64, token):
        # get user from hashed user PK
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except:
            user = None

        # validate token
        if user:
            token_is_valid = account_activation_token.check_token(user, token)

        # validates user email
        if token_is_valid:
            user.is_active = True
            user.save()

            return Response("validation success", status=status.HTTP_201_CREATED)
        
        return Response("validation error", status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    def post(self, request):
        email=request.data
        user = User.objects.get(email=email)
        if user:
            # generate confirmation email
            current_site = get_current_site(self.request)
            send_mail(
                subject='Your passwords has been reset',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                message = render_to_string('authentication/password_reset.html', {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                }),
            )

            return Response("email sent successfully", status=status.HTTP_200_OK)
        
        return Response('no user with this email exists', status=status.HTTP_400_BAD_REQUEST)
    
class NewPassword(APIView):
    def post(self, request, uidb64, token):
        print(request.data, uidb64, token)
        # get user from hashed user PK
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except:
            user = None

        # validate token
        if user:
            token_is_valid = password_reset_token.check_token(user, token)

        # validates user email
        if token_is_valid:
            user.set_password(request.data)
            user.save()
            return Response("password changed successfully", status=status.HTTP_200_OK)
        
        return Response('password reset failed', status=status.HTTP_400_BAD_REQUEST)