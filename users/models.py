from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser

COUNTRIES = (
    ("AG", "Aguascalientes"),
    ("BC", "Baja California"),
    ("BS", "Baja California Sur"),
    ("CM", "Campeche"),
    ("CS", "Chiapas"),
    ("CH", "Chihuahua"),
    ("CO", "Coahuila"),
    ("CL", "Colima"),
    ("DF", "Ciudad de Mexico"),
    ("DG", "Durango"),
    ("GT", "Guanajuato"),
    ("GR", "Guerrero"),
    ("HG", "Hidalgo"),
    ("JA", "Jalisco"),
    ("MX", "Mexico"),
    ("MI", "Michoacan"),
    ("MO", "Morelos"),
    ("NA", "Nayarit"),
    ("NL", "Nuevo Leon"),
    ("OA", "Oaxaca"),
    ("PU", "Puebla"),
    ("QT", "Queretaro"),
    ("QR", "Quintana Roo"),
    ("SL", "San Luis Potosi"),
    ("SI", "Sinaloa"),
    ("SO", "Sonora"),
    ("TB", "Tabasco"),
    ("TM", "Tamaulipas"),
    ("TL", "Tlaxcala"),
    ("VE", "Veracruz"),
    ("YU", "Yucatan"),
    ("ZA", "Zacatecas"),
)


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
    slug = models.SlugField(blank=True)
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.slug = f"{self.username}"
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

class Cliente(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(verbose_name="Foto de perfil", default='default.jpg', upload_to='profile_pics')
    nombre = models.CharField(
        verbose_name="Nombre o Razon social(empresas)",
        max_length=100)
    ape_pat = models.CharField(
        verbose_name="Apellido paterno", max_length=100, blank=True)
    ape_mat = models.CharField(
        verbose_name="Apellido materno", max_length=100, blank=True)
    telefono = models.CharField(verbose_name="Numero teléfonico a 10 digitos", max_length=100)
    calle = models.CharField(verbose_name="Calle", max_length=100)
    num_ext = models.CharField(verbose_name="Numero exterior", max_length=100)
    num_int = models.CharField(verbose_name="Numero interior", max_length=100, blank=True)
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio o alcadía", max_length=100,)
    cp = models.CharField(verbose_name="Código postal",max_length=100,)
    estado = models.CharField(verbose_name="Estado", choices=COUNTRIES, max_length=40)
    slug = models.SlugField(blank=True)
    conektaId = models.CharField(verbose_name="Conekta ID", max_length=30, blank=True)
    es_validado = models.BooleanField(default=False)
    file_import = models.FileField(upload_to='csvImports', max_length=254, default='default.csv')
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        self.slug = f"{self.user.username}"
        super(Cliente, self).save(*args, **kwargs)
    
    @property
    def has_info(self):
        return False if not self.telefono and not self.municipio else True
    
    @property
    def full_name(self):
        return f"{self.nombre} {self.ape_pat} {self.ape_mat}"

class DatosFiscales(models.Model):
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
    estado = models.CharField(verbose_name="Estado", choices=COUNTRIES, max_length=40)
    telefono = models.CharField(verbose_name="Numero teléfonico", max_length=30)
    rfc = models.CharField(max_length=30)
    es_empresa = models.BooleanField(
        verbose_name="Persona moral",
        default=False,
        help_text="Las empresas son personas morales")
    verificador_foto = models.ImageField(verbose_name="Foto de encierro de verificador", upload_to='verificaciones', blank=True)
    verificador_direccion = models.CharField(verbose_name="Dirección del domicilio fiscal", max_length=200, blank=True)
    es_verificado = models.BooleanField(default=False)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

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