from django.contrib import admin
from .models import MyUser, DatosFiscales, Cliente, Transportista

admin.site.register(MyUser)
admin.site.register(DatosFiscales)
admin.site.register(Cliente)
admin.site.register(Transportista)