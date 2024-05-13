from django.urls import path

from .views import (
    UserAPIView,
    ActivateUserApiView,
    UserLoginView,
    SendPasswordResetEmailView,
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
        "cambio-password/", SendPasswordResetEmailView.as_view(), name="reset-password"
    ),
]
