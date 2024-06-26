from typing import Final
from django.urls import path

from .views import (
    UserAPIView,
    ActivateUserApiView,
    UserLoginView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    DatosFiscalesAPIView,
    ContactoAPIView,
    ContactoListAPIView,
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
    path(f"{constants.URL_USUARIO}/login", UserLoginView.as_view(), name="login"),
    path(
        f"{constants.URL_USUARIO}/email-cambio-password/", SendPasswordResetEmailView.as_view(), name="email-reset-password"
    ),
    path(f"{constants.URL_USUARIO}/cambio-password/<uidb64>/<token>/", UserPasswordResetView.as_view(), name='reset-password'),
    path(f"{constants.URL_USUARIO}/datos-fiscales", DatosFiscalesAPIView.as_view(), name='datos-fiscales'),
] + urlpatterns_contacto
