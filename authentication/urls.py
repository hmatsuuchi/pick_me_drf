from django.urls import path
# VIEWS
from .views import SessionLoginView, SessionLogoutView, CreateAccountView, CreateAccountConfirmationView, CreateAccountVerifyView, RecoverPasswordView, RecoverPasswordConfirmationView

urlpatterns = [
    # AUTHENTICATION
    path('session-login', SessionLoginView.as_view(), name="session_login_view"),
    path('session-logout', SessionLogoutView.as_view(), name="session_logout_view"),
    # ACCOUNT CREATION
    path('create-account', CreateAccountView.as_view(), name="create_account_view"),
    path('create-account-confirmation', CreateAccountConfirmationView.as_view(), name="create_account_confirmation_view"),
    path('create-account-verify/<uidb64>/<token>', CreateAccountVerifyView.as_view(), name="create_account_verify_view"),
    # PASSWORD RECOVERY
    path('recover-password', RecoverPasswordView.as_view(), name="recover_password_view"),
    path('recover-password-confirmation', RecoverPasswordConfirmationView.as_view(), name="recover_password_confirmation_view"),
]
