from django.contrib import admin
from .models import Encierros, Unidades, Transportistas, LicenciasTransportistas

admin.site.register(Encierros)
admin.site.register(Unidades)
admin.site.register(Transportistas)
admin.site.register(LicenciasTransportistas)

# Register your models here.
