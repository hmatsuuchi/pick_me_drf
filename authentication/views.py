from django.views.generic import TemplateView, FormView, View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# MODELS
from django.contrib.auth.models import User, Group
from user_profile.models import UserProfile
# FORMS
from .forms import SessionAuthenticationForm, CreateAccountForm, RecoverPasswordForm
# AUTOMATED EMAIL
from django.core.mail import send_mail
from django.conf import settings
# TOKEN GENERATOR
from .tokens import account_activation_token

# ======= AUTHENTICATION =======

# LOGIN
class SessionLoginView(FormView):
    template_name = "authentication/session-login/index.html"
    form_class = SessionAuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        username_cleaned = form.cleaned_data['username']
        password_cleaned = form.cleaned_data['password']

        user = authenticate(username=username_cleaned, password=password_cleaned)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'invalid username or password')
            return redirect("session_login_view")

# LOGOUT
class SessionLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "authentication/session-logout/index.html")
    
# ======= CREATE ACCOUNT =======

# CREATE ACCOUNT
class CreateAccountView(FormView):
    template_name = "authentication/create-account/index.html"
    form_class = CreateAccountForm
    success_url = "/authentication/create-account-confirmation"

    def form_valid(self, form):
        username_cleaned = form.cleaned_data['username']
        email_cleaned = form.cleaned_data['email']
        password_1_cleaned = form.cleaned_data['password_1']
        password_2_cleaned = form.cleaned_data['password_2']

        # data validation - checks if passwords match
        passwords_match = True
        if password_1_cleaned and password_2_cleaned and (password_1_cleaned != password_2_cleaned):
            passwords_match = False
            messages.error(self.request, 'passwords do not match')

        # data validation - checks if username already exists
        try:
            username_exists = User.objects.get(username=username_cleaned)
            messages.error(self.request, 'username is already taken')
        except:
            username_exists = False

        if passwords_match and not username_exists:
            # creates user
            new_user = User()
            new_user.username = username_cleaned
            new_user.email = email_cleaned
            new_user.set_password(password_1_cleaned)
            new_user.is_active = False
            new_user.save()
            # creates user profile
            new_profile = UserProfile()
            new_profile.user = new_user
            new_profile.save()
            # adds user to group
            general_users_group = Group.objects.get(name='general_users')
            general_users_group.user_set.add(new_user)

            # context for email template
            current_site = get_current_site(self.request)
            # generates and sends account confirmation email
            send_mail(
                subject='Verify your account',
                # message='Click the link below to verify your account.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email],
                message = render_to_string('authentication/create-account/email_verification.html',
                {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                 })
            )

            return super().form_valid(form)
        else:
            return redirect("create_account_view")
        
# CREATE ACCOUNT CONFIRMATION
class CreateAccountConfirmationView(TemplateView):
    template_name = "authentication/create-account-confirmation/index.html"

# VERIFY ACCOUNT
class CreateAccountVerifyView(TemplateView):
    template_name = "authentication/create-account-verify/index.html"
# ======= RECOVER PASSWORD =======

# RECOVER PASSWORD
# to prevent authentication information leaks, even unsuccessful account lookups will redirect to the same page
class RecoverPasswordView(FormView):
    template_name = "authentication/recover-password/index.html"
    form_class = RecoverPasswordForm
    success_url = "/authentication/recover-password-confirmation"

    def form_valid(self, form):
        email_cleaned = form.cleaned_data['email']

        try:
            user = User.objects.get(email=email_cleaned)
        except:
            user = None
            
        return redirect("recover_password_confirmation_view")
    
# RECOVER PASSWORD CONFIRMATION
class RecoverPasswordConfirmationView(TemplateView):
    template_name = "authentication/recover-password-confirmation/index.html"