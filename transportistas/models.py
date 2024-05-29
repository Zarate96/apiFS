import datetime
from django.db import models
from django.utils.text import slugify
from accounts.models import MyUser
from shared.constants import constants
from shared.validators import phone_validator, cp_validator

YEAR_CHOICES = [(year, year) for year in range(1950, datetime.date.today().year + 1)]


class Transportistas(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    foto_perfil = models.ImageField(
        "Foto de perfil", default="default.jpg", upload_to="profile_pics"
    )
    nombre = models.CharField("Nombre o Razón Social", max_length=100)
    ape_pat = models.CharField(
        "Apellido paterno", max_length=100, blank=True, default=""
    )
    ape_mat = models.CharField(
        "Apellido materno", max_length=100, blank=True, default=""
    )
    telefono = models.CharField(
        "Número telefónico", max_length=10, validators=[phone_validator]
    )
    calle = models.CharField("Calle", max_length=100)
    num_ext = models.CharField("Número exterior", max_length=100)
    num_int = models.CharField("Número interior", max_length=100, blank=True)
    colonia = models.CharField("Colonia", max_length=100)
    municipio = models.CharField("Municipio", max_length=100)
    cp = models.CharField("Código postal", max_length=5, validators=[cp_validator])
    estado = models.CharField("Estado", choices=constants.STATE_CHOICES, max_length=40)
    calificacion = models.IntegerField("Calificación", default=5)
    viajes_realizados = models.IntegerField("Viajes realizados", default=0)
    notificacion_administrador = models.TextField(
        "Notificaciones para el transportista", blank=True
    )
    es_verificado = models.BooleanField(default=False)
    direccion_google = models.CharField(max_length=200, blank=True)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"

    def __str__(self):
        return f"{self.user.username}"

    # Improved properties
    @property
    def has_encierros(self):
        return Encierros.objects.filter(user=self.user.transportistas).exists()

    @property
    def has_unidades(self):
        return Unidades.objects.filter(user=self.user.transportistas).exists()

    @property
    def has_licencia_conducir(self):
        return LicenciasTransportistas.objects.filter(
            user=self.user.transportistas, tipo_licencia="Licencia conducir"
        ).exists()

    @property
    def has_licencia_mp(self):
        return LicenciasTransportistas.objects.filter(
            user=self.user.transportistas, tipo_licencia="Licencia material peligroso"
        ).exists()

    # @property
    # def has_verificacion(self):
    #     return Verificaciones.objects.filter(transportista=self).exists()


class Encierros(models.Model):
    user = models.ForeignKey(Transportistas, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre de encierro", max_length=50)
    calle = models.CharField("Calle", max_length=100)
    num_ext = models.CharField("Número exterior", max_length=100)
    num_int = models.CharField("Número interior", max_length=100, blank=True)
    colonia = models.CharField("Colonia", max_length=100)
    municipio = models.CharField("Municipio o alcaldía", max_length=100)
    cp = models.CharField("Código postal", max_length=6, validators=[cp_validator])
    estado = models.CharField("Estado", choices=constants.STATE_CHOICES, max_length=40)
    es_validado = models.BooleanField("Es válidado por administrador", default=False)
    es_verificado = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=False)
    direccion_google = models.CharField(
        "Dirección generado por Google Maps Api", max_length=200, blank=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Encierro"
        verbose_name_plural = "Encierros"

    def __str__(self):
        return f"{self.nombre} (usuario: {self.user.user.username})"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.user.user.username}-{self.nombre}")
        super(Encierros, self).save(*args, **kwargs)


class LicenciasTransportistas(models.Model):
    user = models.ForeignKey(Transportistas, on_delete=models.CASCADE)
    tipo_licencia = models.CharField(
        "Tipo de licencia",
        choices=constants.TIPOS_LICENCIAS,
        max_length=50,
    )
    licencia = models.CharField("Número de licencia", max_length=50, unique=True)
    fecha_vencimiento = models.DateTimeField("Fecha de vencimiento de la licencia")
    licencia_foto = models.ImageField(
        "Foto de licencia", upload_to="licencias_transportistas"
    )
    verificada = models.BooleanField(default=False)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Licencia de transportista"
        verbose_name_plural = "Licencias de transportistas"

    def __str__(self):
        return f"{self.user.user.username} - {self.tipo_licencia} - {self.licencia}"


class Unidades(models.Model):
    user = models.ForeignKey(Transportistas, on_delete=models.CASCADE)
    encierro = models.ForeignKey(Encierros, on_delete=models.CASCADE)
    marca = models.CharField("Marca", max_length=50)
    modelo = models.CharField("Modelo", max_length=50)
    año = models.IntegerField(
        "Año", choices=YEAR_CHOICES, default=datetime.datetime.now().year
    )
    tipo_caja = models.CharField("Tipo de caja", max_length=50)
    capacidad_carga = models.FloatField("Capacidad de carga (toneladas)")
    placa = models.CharField("Placa", max_length=15, unique=True)
    tarjeta_circulacion = models.CharField(
        "Tarjeta de circulación", max_length=50, unique=True
    )
    tarjeta_circulacion_foto = models.ImageField(
        "Foto de tarjeta de circulación",
        upload_to="tarjetas_circulacion",
        null=True,
        blank=True,
    )
    foto1 = models.ImageField(
        "Foto 1 de unidad",
        upload_to="unidades_pics",
        null=True,
        blank=True,
    )
    foto2 = models.ImageField(
        "Foto 2 de unidad",
        upload_to="unidades_pics",
        null=True,
        blank=True,
    )
    es_verificado = models.BooleanField("Unidad verificada", default=False)
    creado_at = models.DateTimeField(auto_now_add=True, editable=False)
    modificado_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"

    def __str__(self):
        # More informative representation including the `marca`, `modelo`, and `año`.
        return f"{self.marca} {self.modelo} ({self.año}) - Placa: {self.placa}"
