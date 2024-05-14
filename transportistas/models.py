import datetime
from django.db import models
from django.utils.text import slugify
from accounts.models import MyUser
from shared.constants import constants
from shared.validators import phone_validator, cp_validator

YEAR_CHOICES = [(year, year) for year in range(1950, datetime.date.today().year + 1)]


class Encierro(models.Model):
    nombre = models.CharField(verbose_name="Nombre de encierro", max_length=50)
    calle = models.CharField(verbose_name="Calle", max_length=100)
    external_number = models.CharField(verbose_name="Número exterior", max_length=10)
    internal_number = models.CharField(
        verbose_name="Número interior", max_length=10, blank=True
    )
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio o alcaldía", max_length=100)
    cp = models.CharField(
        verbose_name="Código postal", max_length=5
    )  # Consider adding validators
    estado = models.CharField(verbose_name="Estado", choices=constants.COUNTRIES, max_length=40)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    verificador_foto_encierro = models.ImageField(
        verbose_name="Foto de encierro de verificador",
        upload_to="verificaciones",
        blank=True,
        null=True,
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


class Unidades(models.Model):
    marca = models.CharField(verbose_name="Marca", max_length=50)
    modelo = models.CharField(verbose_name="Modelo", max_length=50)
    año = models.IntegerField(
        verbose_name="Año", choices=YEAR_CHOICES, default=datetime.datetime.now().year
    )
    tipo_caja = models.CharField(verbose_name="Tipo de caja", max_length=50)
    capacidad_carga = models.FloatField(verbose_name="Capacidad de carga (toneladas)")
    placa = models.CharField(
        verbose_name="Placa", max_length=15, unique=True
    )  # Reduced length and made unique
    tarjeta_circulacion = models.CharField(
        verbose_name="Tarjeta de circulación", max_length=50, unique=True
    )  # Made unique
    tarjeta_circulacion_foto = models.ImageField(
        verbose_name="Foto de tarjeta de circulación",
        upload_to="tarjetas_circulacion",
        null=True,
        blank=True,
    )
    tarjeta_circulacion_verificador_foto = models.ImageField(
        verbose_name="Foto de tarjeta de circulación del verificador",
        upload_to="verificaciones",
        blank=True,
        null=True,
    )
    foto1 = models.ImageField(
        verbose_name="Foto 1 de unidad",
        upload_to="unidades_pics",
        null=True,
        blank=True,
    )
    foto2 = models.ImageField(
        verbose_name="Foto 2 de unidad",
        upload_to="unidades_pics",
        null=True,
        blank=True,
    )
    encierro = models.ForeignKey(Encierro, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    verificador_foto_unidad = models.ImageField(
        verbose_name="Foto de unidad del verificador",
        upload_to="verificaciones",
        blank=True,
        null=True,
    )
    es_verificado = models.BooleanField(verbose_name="Unidad verificada", default=False)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        constraints = [
            models.UniqueConstraint(
                fields=["marca", "modelo", "año", "user"], name="unique_unidad_user"
            )
        ]

    def __str__(self):
        # More informative representation including the `marca`, `modelo`, and `año`.
        return f"{self.marca} {self.modelo} ({self.año}) - Placa: {self.placa}"

    @property
    def is_verificado(self):
        return self.es_verificado


class Transportista(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        verbose_name="Foto de perfil", default="default.jpg", upload_to="profile_pics"
    )
    nombre = models.CharField(verbose_name="Nombre o Razón Social", max_length=100)
    ape_pat = models.CharField(
        verbose_name="Apellido paterno", max_length=100, blank=True, default=""
    )
    ape_mat = models.CharField(
        verbose_name="Apellido materno", max_length=100, blank=True, default=""
    )
    telefono = models.CharField(
        verbose_name="Número telefónico", max_length=10, validators=[phone_validator]
    )
    calle = models.CharField(verbose_name="Calle", max_length=100)
    num_ext = models.CharField(verbose_name="Número exterior", max_length=100)
    num_int = models.CharField(
        verbose_name="Número interior", max_length=100, blank=True, null=True
    )
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(verbose_name="Municipio", max_length=100)
    cp = models.CharField(
        verbose_name="Código postal", max_length=5, validators=[cp_validator]
    )
    estado = models.CharField(verbose_name="Estado", choices=constants.COUNTRIES, max_length=40)
    calificacion = models.IntegerField(verbose_name="Calificación", default=5)
    viajes_realizados = models.IntegerField(verbose_name="Viajes realizados", default=0)
    licencia_conducir = models.CharField(
        verbose_name="Número de licencia de conducir",
        max_length=50,
        blank=True,
        null=True,
        unique=True,
    )
    fecha_vencimiento_licencia = models.DateTimeField(
        verbose_name="Fecha de vencimiento de la licencia de manejo",
        blank=True,
        null=True,
    )
    licencia_conducir_foto = models.ImageField(
        verbose_name="Foto de licencia de conducir",
        upload_to="licencias_transportistas",
        blank=True,
        null=True,
    )
    licencia_conducir_verificador_foto = models.ImageField(
        verbose_name="Foto de licencia de conducir de verificador",
        upload_to="verificaciones",
        blank=True,
        null=True,
    )
    licencia_mp = models.BooleanField(
        default=False, verbose_name="Permiso de transportación de material peligroso"
    )
    licencia_conducir_mp_foto = models.ImageField(
        verbose_name="Foto de permiso para conducir material peligroso",
        upload_to="licencias_transportistas",
        blank=True,
        null=True,
    )
    licencia_conducir_mp_verificador_foto = models.ImageField(
        verbose_name="Foto de permiso para conducir material peligroso de verificador",
        upload_to="verificaciones",
        blank=True,
        null=True,
    )
    notificacion_administrador = models.TextField(
        verbose_name="Notificaciones para el transportista", blank=True, null=True
    )
    es_validado = models.BooleanField(default=False)
    es_verificado = models.BooleanField(default=False)
    es_activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"

    def __str__(self):
        return (
            f"{self.nombre} {self.ape_pat} {self.ape_mat}".strip() or self.user.username
        )

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

    # @property
    # def has_verificacion(self):
    #     return Verificaciones.objects.filter(transportista=self).exists()
