from django_filters import rest_framework as filters
from .models import Encierros, Unidades

class EncierroFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    calle = filters.CharFilter(field_name='calle', lookup_expr='icontains')
    colonia = filters.CharFilter(field_name='colonia', lookup_expr='icontains')
    municipio = filters.CharFilter(field_name='municipio', lookup_expr='icontains')
    estado = filters.CharFilter(field_name='estado', lookup_expr='exact')
    cp = filters.CharFilter(field_name='cp', lookup_expr='exact')
    es_verificado = filters.BooleanFilter(field_name='es_verificado', lookup_expr='exact')
    es_activo = filters.BooleanFilter(field_name='es_activo', lookup_expr='exact')

    class Meta:
        model = Encierros
        fields = ['nombre', 'calle', 'colonia', 'municipio', 'estado', 'cp', 'es_verificado', 'es_activo']


class UnidadesFilter(filters.FilterSet):
    marca = filters.CharFilter(field_name='marca', lookup_expr='icontains')
    modelo = filters.CharFilter(field_name='modelo', lookup_expr='icontains')
    placa = filters.CharFilter(field_name='placa', lookup_expr='exact')
    tipo_caja = filters.CharFilter(field_name='tipo_caja', lookup_expr='exact')
    capacidad_carga = filters.NumberFilter(field_name='capacidad_carga', lookup_expr='exact')
    encierro = filters.CharFilter(field_name='encierro', lookup_expr='exact')
    es_activo = filters.BooleanFilter(field_name='es_activo', lookup_expr='exact')

    class Meta:
        model = Unidades
        fields = ['marca', 'modelo', 'placa', 'tipo_caja', 'capacidad_carga', 'encierro', 'es_activo']
