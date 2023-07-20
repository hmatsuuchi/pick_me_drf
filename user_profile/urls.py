from django.urls import path
from .views import GetLoggedInUserData

urlpatterns = [
     path('get_logged_in_user_data/', GetLoggedInUserData.as_view(), name ='user_profile_view'),
]