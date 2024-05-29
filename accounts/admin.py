from django.contrib import admin
from .models import MyUser, DatosFiscales, Contactos

admin.site.register(MyUser)
admin.site.register(DatosFiscales)
admin.site.register(Contactos)

