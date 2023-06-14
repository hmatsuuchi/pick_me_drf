from django.urls import path
# VIEWS
from .views import MainSpaView

urlpatterns = [
    # MAIN SPA
    path('', MainSpaView.as_view(), name="main_spa_view"),
]
