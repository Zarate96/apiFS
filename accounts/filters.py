from django_filters import rest_framework as filters
from .models import Contactos

class ContactoFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    telefono = filters.CharFilter(field_name='telefono', lookup_expr='icontains')
    correo = filters.CharFilter(field_name='correo', lookup_expr='icontains')

    class Meta:
        model = Contactos
        fields = ['nombre', 'telefono', 'correo']

