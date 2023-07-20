from django.contrib import admin
from django.urls import path, include
# URLS
import authentication.urls as AuthenticationUrls
import user_profile.urls as UserProfileUrls

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    # API - AUTHENTICATION
    path('authentication/', include(AuthenticationUrls)),
    # API - USER PROFILE
    path('user_profile/', include(UserProfileUrls)),
]
