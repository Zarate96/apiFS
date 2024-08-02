from django.db import models
from django.utils.text import slugify

from accounts.models import MyUser

from shared.constants import constants
from shared.validators import phone_validator, cp_validator


class Clientes(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    foto_perfil = models.ImageField(
        "Foto de perfil", default="default.jpg", upload_to="profile_pics"
    )
    nombre = models.CharField("Nombre o Razon social(empresas)", max_length=100)
    ape_pat = models.CharField("Apellido paterno", max_length=100, blank=True)
    ape_mat = models.CharField("Apellido materno", max_length=100, blank=True)
    telefono = models.CharField(
        "Numero teléfonico a 10 digitos", max_length=11, validators=[phone_validator]
    )
    calle = models.CharField("Calle", max_length=100)
    num_ext = models.CharField("Numero exterior", max_length=100)
    num_int = models.CharField("Numero interior", max_length=100, blank=True)
    colonia = models.CharField("Colonia", max_length=100)
    municipio = models.CharField(
        "Municipio o alcadía",
        max_length=100,
    )
    cp = models.CharField("Código postal", max_length=6, validators=[cp_validator])
    estado = models.CharField("Estado", choices=constants.STATE_CHOICES, max_length=40)
    conektaId = models.CharField("Conekta ID", max_length=30, blank=True)
    es_validado = models.BooleanField(default=False)
    file_import = models.FileField(
        upload_to="csvImports", max_length=254, default="default.csv"
    )
    direccion_google = models.CharField(max_length=200, blank=True, null=True)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return str(self.user.username)

    @property
    def has_info(self):
        return False if not self.telefono and not self.municipio else True

    @property
    def nombreOrRazon(self):
        return (
            f"{self.nombre}"
            if self.user.es_empresa
            else f"{self.nombre} {self.ape_pat} {self.ape_mat}"
        )
    
    @property
    def has_domicilios(self):
        return self.domicilios_set.exists()

class Domicilios(models.Model):
    user = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre para identificar domicilio", max_length=200)
    calle = models.CharField("Calle", max_length=200)
    num_ext = models.CharField("Numero exterior", max_length=200)
    num_int = models.CharField("Numero interior", max_length=200, blank=True)
    colonia = models.CharField("Colonia", max_length=200)
    municipio = models.CharField("Municipio o alcadía", max_length=200)
    cp = models.CharField("Código postal",max_length=200,)
    estado = models.CharField("Estado", choices=constants.STATE_CHOICES, max_length=100)
    referencias = models.TextField("Refrencias del domicilio")
    longitud = models.FloatField("Longitud", blank=True)
    latitud = models.FloatField("Latitud", blank=True)
    es_valida = models.BooleanField("Es válido", default=False)
    formato_google = models.CharField("Dirección completa", max_length=200, blank=True)
    id_google = models.CharField("Google place ID", max_length=250, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=250)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Domicilios"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.user.user.username}-{self.nombre}")
        return super(Domicilios, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.nombre} - {self.user.user.username}'
    
    @property
    def direccion_completa(self):
        return f'{self.calle } {self.num_ext} {self.num_int}, C.P  {self.cp}  {self.colonia}  {self.municipio},  {self.estado}'