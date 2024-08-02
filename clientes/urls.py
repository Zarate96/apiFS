from django.urls import path
from .views import ClienteAPIView, DomiciliosAPIView, DomiciliosListAPIView
from shared.constants import constants

urlpatterns_dom = [
    path(
        f"{constants.URL_CLIENTE}/domicilios/list/",
        DomiciliosListAPIView.as_view(),
        name="domicilios-list",
    ),
    path(
        f"{constants.URL_CLIENTE}/domicilios/",
        DomiciliosAPIView.as_view(),
        name="domicilios-management",
    ),
    path(
        f"{constants.URL_CLIENTE}/domicilios/<str:slug>/",
        DomiciliosAPIView.as_view(),
        name="domicilios-detail",
    ),
]

urlpatterns = [
    path(
        f"{constants.URL_CLIENTE}/perfil",
        ClienteAPIView.as_view(),
        name="cliente-management",
    ),
] + urlpatterns_dom
