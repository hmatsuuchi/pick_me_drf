from django.contrib import admin
from django.urls import path, include
# URLS
import authentication.urls as AuthenticationUrls

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # AUTHENTICATION
    path('authentication/', include(AuthenticationUrls)),
]
