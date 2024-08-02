from typing import Final
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserAPIView,
    ActivateUserApiView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    DatosFiscalesAPIView,
    ContactoAPIView,
    ContactoListAPIView,
    UserProfileAPIView,
    MyTokenObtainPairView,
)

from shared.constants import constants

urlpatterns_contacto = [
    path(f"{constants.URL_USUARIO}/contactos/", ContactoListAPIView.as_view(), name="contacto-list"),
    path(f"{constants.URL_USUARIO}/contactos/agregar", ContactoAPIView.as_view(), name="contacto-management-add"),
    path(f"{constants.URL_USUARIO}/contactos/<int:pk>", ContactoAPIView.as_view(), name="contacto-management"),
]

urlpatterns = [
    path(f"{constants.URL_USUARIO}/registro", UserAPIView.as_view(), name="register"),
    path(
        f"{constants.URL_USUARIO}/activar-usario/<uidb64>/<token>",
        ActivateUserApiView.as_view(),
        name="activate",
    ),
    path(f"{constants.URL_USUARIO}/token", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{constants.URL_USUARIO}/refresh", TokenRefreshView.as_view()),
    path(f"{constants.URL_USUARIO}/perfil/<user_id>", UserProfileAPIView.as_view(), name="user-profile"),
    path(
        f"{constants.URL_USUARIO}/email-cambio-password/", SendPasswordResetEmailView.as_view(), name="email-reset-password"
    ),
    path(f"{constants.URL_USUARIO}/cambio-password/<uidb64>/<token>/", UserPasswordResetView.as_view(), name='reset-password'),
    path(f"{constants.URL_USUARIO}/datos-fiscales", DatosFiscalesAPIView.as_view(), name='datos-fiscales'),
] + urlpatterns_contacto
