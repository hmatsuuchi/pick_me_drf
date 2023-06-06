from django.urls import path
# VIEWS
from .views import SessionLoginView, SessionLogoutView, SessionAuthenticateView

urlpatterns = [
    path('session-login', SessionLoginView.as_view(), name="session_login_view"),
    path('session-logout', SessionLogoutView.as_view(), name="session_logout_view"),
    path('session-authenticate', SessionAuthenticateView.as_view(), name="session_authenticate_view")
]
