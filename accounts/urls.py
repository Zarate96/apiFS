from django.urls import path

from .views import (
    UserAPIView,
    ActivateUserApiView,
    UserLoginView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    DatosFiscalesAPIView
)

urlpatterns = [
    path("registro", UserAPIView.as_view(), name="register"),
    path(
        "activar-usario/<uidb64>/<token>",
        ActivateUserApiView.as_view(),
        name="activate",
    ),
    path("login", UserLoginView.as_view(), name="login"),
    path(
        "email-cambio-password/", SendPasswordResetEmailView.as_view(), name="email-reset-password"
    ),
    path('cambio-password/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('datos-fiscales/<slug>', DatosFiscalesAPIView.as_view(), name='datos-fiscales')
]
