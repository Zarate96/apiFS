from django.db import models
from shared.constants import constants
from accounts.models import MyUser

class Cliente(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        verbose_name="Foto de perfil", default="default.jpg", upload_to="profile_pics"
    )
    nombre = models.CharField(
        verbose_name="Nombre o Razon social(empresas)", max_length=100
    )
    ape_pat = models.CharField(
        verbose_name="Apellido paterno", max_length=100, blank=True
    )
    ape_mat = models.CharField(
        verbose_name="Apellido materno", max_length=100, blank=True
    )
    telefono = models.CharField(
        verbose_name="Numero teléfonico a 10 digitos", max_length=100
    )
    calle = models.CharField(verbose_name="Calle", max_length=100)
    num_ext = models.CharField(verbose_name="Numero exterior", max_length=100)
    num_int = models.CharField(
        verbose_name="Numero interior", max_length=100, blank=True
    )
    colonia = models.CharField(verbose_name="Colonia", max_length=100)
    municipio = models.CharField(
        verbose_name="Municipio o alcadía",
        max_length=100,
    )
    cp = models.CharField(
        verbose_name="Código postal",
        max_length=100,
    )
    estado = models.CharField(verbose_name="Estado", choices=constants.COUNTRIES, max_length=40)
    conektaId = models.CharField(verbose_name="Conekta ID", max_length=30, blank=True)
    es_validado = models.BooleanField(default=False)
    file_import = models.FileField(
        upload_to="csvImports", max_length=254, default="default.csv"
    )
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
