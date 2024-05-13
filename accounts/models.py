from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from shared.constants import constants

class MyUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    penalizaciones = models.IntegerField(
        verbose_name="Número de penalizaciones", default=0
    )
    es_transportista = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=False)
    es_verificador = models.BooleanField(default=False)
    es_empresa = models.BooleanField(
        verbose_name="Persona moral",
        default=False,
        help_text="Las empresas son personas morales",
    )
    slug = models.SlugField(unique=True, blank=True, max_length=100, allow_unicode=True)
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(MyUser, self).save(*args, **kwargs)
    
    @property
    def is_cliente(self):
        return self.es_cliente
    
    @property
    def is_transportista(self):
        return self.es_transportista
    
    @property
    def is_verificador(self):
        return self.es_verificador
    
    @property
    def is_empresa(self):
        return self.es_empresa

    @property
    def has_datos_fiscales(self):
        return hasattr(self, "datosfiscales")

class DatosFiscales(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(
        verbose_name="Nombre o Razon social(empresas)",
        max_length=100)
    ape_pat = models.CharField(
        verbose_name="Apellido paterno", max_length=100, blank=True)
    ape_mat = models.CharField(
        verbose_name="Apellido materno", max_length=100,blank=True)
    calle = models.CharField(verbose_name="Calle", max_length=100)
    num_ext = models.CharField(verbose_name="Numero exterior", max_length=100)
    num_int = models.CharField(verbose_name="Numero interior", max_length=100, blank=True)
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio o alcadía", max_length=100)
    cp = models.CharField(verbose_name="Código postal",max_length=100,)
    estado = models.CharField(verbose_name="Estado", choices=constants.COUNTRIES, max_length=40)
    telefono = models.CharField(verbose_name="Numero teléfonico", max_length=30)
    rfc = models.CharField(max_length=30)
    es_empresa = models.BooleanField(
        verbose_name="Persona moral",
        default=False,
        help_text="Las empresas son personas morales")
    verificador_foto = models.ImageField(verbose_name="Foto de encierro de verificador", upload_to='verificaciones', blank=True)
    es_verificado = models.BooleanField(default=False)
    direccion_google = models.CharField(max_length=200, blank=True, null=True)

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
    def is_verified(self):
        return self.es_verificado
    
    @property
    def direccion_completa(self):
        return f'{self.calle } {self.num_ext} {self.num_int}, C.P  {self.cp}  {self.colonia}  {self.municipio},  {self.estado}'

    @property
    def nombreOrRazon(self):
        return f'{self.nombre}' if self.es_empresa else f'{self.nombre} {self.ape_pat} {self.ape_mat}'
            
    def __str__(self):
        return f'{self.rfc} de {self.user.username}'