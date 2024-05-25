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

# Licencias chnange order path in next clean database and reset migrations
# AGREGAR DOS TRANSPORTISTAS Y PROBAR TODOS EL CRUD DE TRANSPORTISTASS
# CHECK NEW URL FOR ALL
# TEST ALL WITHOUT SLUG ONY FOR CURRENT USER

urlpatterns_licencias = [
    path(
        f"{constants.URL_TRANSPORTISTA}/licencias/",
        LicenciasTransportistasAPIView.as_view(),
        name="licencias-transportistas-management",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/licencia-conducir/",
        LicenciasTransportistasAPIView.as_view(),
        name="licencia-conducir-management",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/licencia-mp/",
        LicenciasTransportistasAPIView.as_view(),
        name="licencia-mp-management",
    ),
]

urlpatterns_unidades = [
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/unidades",
        ListUnidadesAPIView.as_view(),
        name="unidades-list",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/unidades/agregar",
        UnidadesAPIView.as_view(),
        name="unidades-management-add",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/unidades/<str:placa>",
        UnidadesAPIView.as_view(),
        name="unidades-management",
    ),    
]

urlpatterns_encierros = [
    # Encierros
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/encierros",
        ListEncierrosAPIView.as_view(),
        name="encierro-list",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/encierros/agregar",
        EncierroAPIView.as_view(),
        name="encierro-management-add",
    ),
    path(
        f"{constants.URL_TRANSPORTISTA}/<str:slug>/encierros/<str:encierro_slug>",
        EncierroAPIView.as_view(),
        name="encierro-management",
    ),
]


urlpatterns = (
    [
        path(
            f"{constants.URL_TRANSPORTISTA}/<str:slug>",
            TransportistaAPIView.as_view(),
            name="transportista-management",
        ),
    ]
    + urlpatterns_licencias
    + urlpatterns_unidades
    + urlpatterns_encierros
)
