from django.contrib import admin
from django.urls import path, include
# URLS
import authentication.urls as AuthenticationUrls
import main_spa.urls as MainSpaUrls

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    # AUTHENTICATION
    path('authentication/', include(AuthenticationUrls)),
    # MAIN SPA
    # this is a temporary routing; acutal routing to react files done by NGINX on deployment
    path('', include(MainSpaUrls)),
]
