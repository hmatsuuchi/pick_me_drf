from django.urls import path
# DJANGO DEFAULT AUTHENTICATION VIEWS
from django.contrib.auth import views as auth_views
# VIEWS
from .views import CreateAccountView, CreateAccountConfirmationView, CreateAccountVerifyView

urlpatterns = [
    # AUTHENTICATION
    # uses default Django authentication views
    path('session-login', auth_views.LoginView.as_view(template_name="authentication/session-login/index.html", next_page="/"), name="session_login_view"), 
    path('session-logout', auth_views.LogoutView.as_view(template_name="authentication/session-logout/index.html"), name="session_logout_view"),
    
    # ACCOUNT CREATION
    # uses custom authentication views
    # create account form -> create account confirmation -> email link -> validate link
    path('create-account', CreateAccountView.as_view(), name="create_account_view"),
    path('create-account-confirmation', CreateAccountConfirmationView.as_view(), name="create_account_confirmation_view"),
    path('create-account-verify/<uidb64>/<token>', CreateAccountVerifyView.as_view(), name="create_account_verify_view"),

    # PASSWORD CHANGE
    # uses default Django authentication views
    path('password-change', auth_views.PasswordChangeView.as_view(template_name="authentication/password-change/index.html", success_url='password-change-done'), name="password_change_view"),
    path('password-change-done', auth_views.PasswordChangeDoneView.as_view(template_name="authentication/password-change-done/index.html"), name="password_change_done_view"),
]
