import datetime
from .validators import phone_validator, cp_validator
from typing import Iterable
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

COUNTRIES = (
    ('Aguascalientes','Aguascalientes'),
    ('Baja California','Baja California'),
    ('Baja California Sur','Baja California Sur'),
    ('Campeche','Campeche'),
    ('Coahuila de Zaragoza','Coahuila de Zaragoza'),
    ('Colima','Colima'),
    ('Chiapas','Chiapas'),
    ('Chihuahua','Chihuahua'),
    ('CDMX','CDMX'),
    ('Durango','Durango'),
    ('Guanajuato','Guanajuato'),
    ('Guerrero','Guerrero'),
    ('Hidalgo','Hidalgo'),
    ('Jalisco','Jalisco'),
    ('México','México'),
    ('Michoacán de Ocampo','Michoacán de Ocampo'),
    ('Morelos','Morelos'),
    ('Nayarit','Nayarit'),
    ('Nuevo León','Nuevo León'),
    ('Oaxaca','Oaxaca'),
    ('Puebla','Puebla'),
    ('Querétaro','Querétaro'),
    ('Quintana Roo','Quintana Roo'),
    ('San Luis Potosí','San Luis Potosí'),
    ('Sinaloa','Sinaloa'),
    ('Sonora','Sonora'),
    ('Tabasco','Tabasco'),
    ('Tamaulipas','Tamaulipas'),
    ('Tlaxcala','Tlaxcala'),
    ('Veracruz de Ignacio de la Llave','Veracruz de Ignacio de la Llave'),
    ('Yucatán','Yucatán'),
    ('Zacatecas','Zacatecas'),
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
    conektaId = models.CharField(verbose_name="Conekta ID", max_length=30, blank=True)
    es_validado = models.BooleanField(default=False)
    file_import = models.FileField(upload_to='csvImports', max_length=254, default='default.csv')
    direccion_google = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return str(self.user.username)
    
    @property
    def has_info(self):
        return False if not self.telefono and not self.municipio else True
    
    @property
    def full_name(self):
        return f"{self.nombre} {self.ape_pat} {self.ape_mat}"

class Encierro(models.Model):
    nombre = models.CharField(verbose_name="Nombre de encierro", max_length=50)
    calle = models.CharField(verbose_name="Calle", max_length=100)
    external_number = models.CharField(verbose_name="Número exterior", max_length=10)
    internal_number = models.CharField(verbose_name="Número interior", max_length=10, blank=True)
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio o alcaldía", max_length=100)
    cp = models.CharField(verbose_name="Código postal", max_length=5)  # Consider adding validators
    estado = models.CharField(verbose_name="Estado", choices=COUNTRIES, max_length=40)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    verificador_foto_encierro = models.ImageField(
        verbose_name="Foto de encierro de verificador", upload_to='verificaciones', blank=True, null=True
    )
    verificador_direccion = models.CharField(
        verbose_name="Dirección del domicilio fiscal", max_length=200, blank=True
    )
    es_validado = models.BooleanField(default=False)
    es_verificado = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = "Encierro"
        verbose_name_plural = "Encierros"

    def __str__(self):
        return f"{self.nombre} (usuario: {self.user.username})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            unique_slug = base_slug
            counter = 1
            while Encierro.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
 
YEAR_CHOICES = [(year, year) for year in range(1950, datetime.date.today().year + 1)]

class Unidades(models.Model):
    marca = models.CharField(verbose_name="Marca", max_length=50)
    modelo = models.CharField(verbose_name="Modelo", max_length=50)
    año = models.IntegerField(verbose_name="Año", choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    tipo_caja = models.CharField(verbose_name="Tipo de caja", max_length=50)
    capacidad_carga = models.FloatField(verbose_name="Capacidad de carga (toneladas)")
    placa = models.CharField(verbose_name="Placa", max_length=15, unique=True)  # Reduced length and made unique
    tarjeta_circulacion = models.CharField(verbose_name="Tarjeta de circulación", max_length=50, unique=True)  # Made unique
    tarjeta_circulacion_foto = models.ImageField(
        verbose_name="Foto de tarjeta de circulación", upload_to='tarjetas_circulacion', null=True, blank=True
    )
    tarjeta_circulacion_verificador_foto = models.ImageField(
        verbose_name="Foto de tarjeta de circulación del verificador", upload_to='verificaciones', blank=True, null=True
    )
    foto1 = models.ImageField(verbose_name="Foto 1 de unidad", upload_to='unidades_pics', null=True, blank=True)
    foto2 = models.ImageField(verbose_name="Foto 2 de unidad", upload_to='unidades_pics', null=True, blank=True)
    encierro = models.ForeignKey(Encierro, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    verificador_foto_unidad = models.ImageField(
        verbose_name="Foto de unidad del verificador", upload_to='verificaciones', blank=True, null=True
    )
    es_verificado = models.BooleanField(verbose_name="Unidad verificada", default=False)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        constraints = [
            models.UniqueConstraint(fields=['marca', 'modelo', 'año', 'user'], name='unique_unidad_user')
        ]

    def __str__(self):
        # More informative representation including the `marca`, `modelo`, and `año`.
        return f'{self.marca} {self.modelo} ({self.año}) - Placa: {self.placa}'
    
    @property
    def is_verificado(self):
        return self.es_verificado

class Transportista(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(verbose_name="Foto de perfil", default='default.jpg', upload_to='profile_pics')
    nombre = models.CharField(verbose_name="Nombre o Razón Social", max_length=100)
    ape_pat = models.CharField(verbose_name="Apellido paterno", max_length=100, blank=True, default="")
    ape_mat = models.CharField(verbose_name="Apellido materno", max_length=100, blank=True, default="")
    telefono = models.CharField(verbose_name="Número telefónico", max_length=10, validators=[phone_validator])
    calle = models.CharField(verbose_name="Calle", max_length=100)
    num_ext = models.CharField(verbose_name="Número exterior", max_length=100)
    num_int = models.CharField(verbose_name="Número interior", max_length=100, blank=True, null=True)
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio", max_length=100)
    cp = models.CharField(verbose_name="Código postal", max_length=5, validators=[cp_validator])
    estado = models.CharField(verbose_name="Estado", choices=COUNTRIES, max_length=40)
    calificacion = models.IntegerField(verbose_name="Calificación", default=5)
    viajes_realizados = models.IntegerField(verbose_name="Viajes realizados", default=0)
    licencia_conducir = models.CharField(verbose_name="Número de licencia de conducir", max_length=50, blank=True, null=True, unique=True)
    fecha_vencimiento_licencia = models.DateTimeField(verbose_name="Fecha de vencimiento de la licencia de manejo", blank=True, null=True)
    licencia_conducir_foto = models.ImageField(verbose_name="Foto de licencia de conducir", upload_to='licencias_transportistas', blank=True, null=True)
    licencia_conducir_verificador_foto = models.ImageField(verbose_name="Foto de licencia de conducir de verificador", upload_to='verificaciones', blank=True, null=True)
    licencia_mp = models.BooleanField(default=False, verbose_name="Permiso de transportación de material peligroso")
    licencia_conducir_mp_foto = models.ImageField(verbose_name="Foto de permiso para conducir material peligroso", upload_to='licencias_transportistas', blank=True, null=True)
    licencia_conducir_mp_verificador_foto = models.ImageField(verbose_name="Foto de permiso para conducir material peligroso de verificador", upload_to='verificaciones', blank=True, null=True)
    notificacion_administrador = models.TextField(verbose_name="Notificaciones para el transportista", blank=True, null=True)
    es_validado = models.BooleanField(default=False)
    es_verificado = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"

    def __str__(self):
        return f'{self.nombre} {self.ape_pat} {self.ape_mat}'.strip() or self.user.username

    def save(self, *args, **kwargs):
        # Automatically set `licencia_mp` based on whether `licencia_conducir_mp_foto` is present
        if self.licencia_conducir_mp_foto:
            self.licencia_mp = True

        super().save(*args, **kwargs)

    # Improved properties
    @property
    def has_unidades(self):
        return Unidades.objects.filter(user=self.user).exists()

    @property
    def has_licencia_conducir(self):
        return bool(self.licencia_conducir and self.licencia_conducir_foto)

    @property
    def is_lc_verificado(self):
        return bool(self.licencia_conducir_verificador_foto)

    @property
    def is_lmp_verificado(self):
        return bool(self.licencia_conducir_mp_verificador_foto)

    @property
    def has_verificacion(self):
        return Verificaciones.objects.filter(transportista=self).exists()

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
    estado = models.CharField(verbose_name="Estado", choices=COUNTRIES, max_length=40)
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