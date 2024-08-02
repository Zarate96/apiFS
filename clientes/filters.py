from django_filters import rest_framework as filters
from .models import Domicilios


class DomiciliosFilter(filters.FilterSet):
    calle = filters.CharFilter(field_name='calle', lookup_expr='icontains')
    colonia = filters.CharFilter(field_name='colonia', lookup_expr='icontains')
    municipio = filters.CharFilter(field_name='municipio', lookup_expr='icontains')
    estado = filters.CharFilter(field_name='estado', lookup_expr='exact')
    cp = filters.CharFilter(field_name='cp', lookup_expr='exact')
    es_valida = filters.BooleanFilter(field_name='es_valida', lookup_expr='exact')

    class Meta:
        model = Domicilios
        fields = ['calle', 'colonia', 'municipio', 'estado', 'cp', 'es_valida']

