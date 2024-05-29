from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from shared.constants import constants
from shared.validators import phone_validator, cp_validator, rfc_validator


class MyUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    penalizaciones = models.IntegerField("Número de penalizaciones", default=0)
    es_transportista = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=False)
    es_verificador = models.BooleanField(default=False)
    es_empresa = models.BooleanField(
        "Persona moral",
        default=False,
        help_text="Las empresas son personas morales",
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        db_table = "auth_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(MyUser, self).save(*args, **kwargs)

    @property
    def has_datos_fiscales(self):
        return hasattr(self, "datosfiscales")


class DatosFiscales(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField("Nombre o Razon social(empresas)", max_length=100)
    ape_pat = models.CharField("Apellido paterno", max_length=100, blank=True)
    ape_mat = models.CharField("Apellido materno", max_length=100, blank=True)
    calle = models.CharField("Calle", max_length=100)
    num_ext = models.CharField("Numero exterior", max_length=100)
    num_int = models.CharField("Numero interior", max_length=100, blank=True)
    colonia = models.CharField("Colonia", max_length=100)
    municipio = models.CharField("Municipio o alcadía", max_length=100)
    cp = models.CharField("Código postal", max_length=100, validators=[cp_validator])
    estado = models.CharField("Estado", choices=constants.STATE_CHOICES, max_length=40)
    telefono = models.CharField(
        "Numero teléfonico", max_length=30, validators=[phone_validator]
    )
    rfc = models.CharField("RFC", max_length=13, validators=[rfc_validator])
    es_empresa = models.BooleanField(
        "Persona moral",
        default=False,
        help_text="Las empresas son personas morales",
    )
    es_verificado = models.BooleanField(default=False)
    direccion_google = models.CharField(
        "Direccón regresada por Google Api", max_length=200, blank=True
    )
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Datos fiscales"
        verbose_name_plural = "Datos fiscales"

    def save(self, *args, **kwargs):
        if self.user.es_empresa:
            self.es_empresa = True
        super(DatosFiscales, self).save(*args, **kwargs)

    @property
    def has_rfc(self):
        return True if self.rfc else False

    @property
    def direccion_completa(self):
        return f"{self.calle } {self.num_ext} {self.num_int}, C.P  {self.cp}  {self.colonia}  {self.municipio},  {self.estado}"

    @property
    def nombreOrRazon(self):
        return (
            f"{self.nombre}"
            if self.es_empresa
            else f"{self.nombre} {self.ape_pat} {self.ape_mat}"
        )

    def __str__(self):
        return f"{self.rfc} de {self.user.username}"


class Contactos(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre", max_length=100)
    ape_pat = models.CharField("Apellido paterno", max_length=100)
    ape_mat = models.CharField("Apellido materno", max_length=100)
    telefono = models.CharField(
        "Numero teléfonico", max_length=50, validators=[phone_validator]
    )
    email = models.EmailField("Correo electronico", max_length=254)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return f"{self.nombre} contacto de {self.user.username} "
