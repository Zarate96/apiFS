from django.urls import path
from .views import ClienteAPIView
from shared.constants import constants

urlpatterns = [
    path(f'{constants.URL_CLIENTE}/perfil', ClienteAPIView.as_view(), name='cliente-management'),
]
