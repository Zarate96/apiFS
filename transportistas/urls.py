from django.urls import path
from .views import (
    TransportistaAPIView,
    LicenciasTransportistasAPIView,
    EncierroAPIView,
    ListEncierrosAPIView,
    ListUnidadesAPIView,
    UnidadesAPIView,
)
from shared.constants import constants

# Validate all with final slash

urlpatterns_licencias = [
    path(
        f"{constants.URL_TRANSPORTISTA}/licencias/conducir/",
        LicenciasTransportistasAPIView.as_view(),
        name="licencia-conducir-management",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/licencias/mp/",
        LicenciasTransportistasAPIView.as_view(),
        name="licencia-mp-management",
    ),
]

urlpatterns_unidades = [
    path(
        f"{constants.URL_TRANSPORTISTA}/unidades/list/",
        ListUnidadesAPIView.as_view(),
        name="unidades-list",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/unidades/",
        UnidadesAPIView.as_view(),
        name="unidades-management",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/unidades/<str:placa>/",
        UnidadesAPIView.as_view(),
        name="unidades-detail",
    ),    
]

urlpatterns_encierros = [
    # Encierros
    path(
        f"{constants.URL_TRANSPORTISTA}/encierros/list/",
        ListEncierrosAPIView.as_view(),
        name="encierro-list",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/encierros/<str:encierro_slug>/",
        EncierroAPIView.as_view(),
        name="encierro-detail",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/encierros/",
        EncierroAPIView.as_view(),
        name="encierro-management",
    ),
]


urlpatterns = (
    [
        path(
            f"{constants.URL_TRANSPORTISTA}/perfil",
            TransportistaAPIView.as_view(),
            name="transportista-management",
        ),
    ]
    + urlpatterns_licencias
    + urlpatterns_unidades
    + urlpatterns_encierros
)
