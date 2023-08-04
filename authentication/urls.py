from django.urls import path
from rest_framework_simplejwt import views as jwt_views
# VIEWS
from . import views

urlpatterns = [
    # JWT authentication
     path('token/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
     path('logout/', views.LogoutView.as_view(), name='logout'),
     # account creation/verification/password reset
     path('account_create/', views.AccountCreate.as_view(), name='account_create'),
     path('account_verify/<uidb64>/<token>', views.AccountVerify.as_view(), name='account_verify'),
     path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
     path('new_password/<uidb64>/<token>', views.NewPassword.as_view(), name='new_password'),
]