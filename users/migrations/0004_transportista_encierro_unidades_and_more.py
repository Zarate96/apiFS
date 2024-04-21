# Generated by Django 5.0.3 on 2024-04-21 03:30

import django.db.models.deletion
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_myuser_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transportista',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Foto de perfil')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre o Razón Social')),
                ('ape_pat', models.CharField(blank=True, default='', max_length=100, verbose_name='Apellido paterno')),
                ('ape_mat', models.CharField(blank=True, default='', max_length=100, verbose_name='Apellido materno')),
                ('telefono', models.CharField(max_length=10, validators=[users.validators.phone_validator], verbose_name='Número telefónico')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('num_ext', models.CharField(max_length=100, verbose_name='Número exterior')),
                ('num_int', models.CharField(blank=True, max_length=100, null=True, verbose_name='Número interior')),
                ('colonia', models.CharField(max_length=100, verbose_name='Colonia')),
                ('municipio', models.CharField(max_length=100, verbose_name='Municipio')),
                ('cp', models.CharField(max_length=5, validators=[users.validators.cp_validator], verbose_name='Código postal')),
                ('estado', models.CharField(choices=[('AG', 'Aguascalientes'), ('BC', 'Baja California'), ('BS', 'Baja California Sur'), ('CM', 'Campeche'), ('CS', 'Chiapas'), ('CH', 'Chihuahua'), ('CO', 'Coahuila'), ('CL', 'Colima'), ('DF', 'Ciudad de Mexico'), ('DG', 'Durango'), ('GT', 'Guanajuato'), ('GR', 'Guerrero'), ('HG', 'Hidalgo'), ('JA', 'Jalisco'), ('MX', 'Mexico'), ('MI', 'Michoacan'), ('MO', 'Morelos'), ('NA', 'Nayarit'), ('NL', 'Nuevo Leon'), ('OA', 'Oaxaca'), ('PU', 'Puebla'), ('QT', 'Queretaro'), ('QR', 'Quintana Roo'), ('SL', 'San Luis Potosi'), ('SI', 'Sinaloa'), ('SO', 'Sonora'), ('TB', 'Tabasco'), ('TM', 'Tamaulipas'), ('TL', 'Tlaxcala'), ('VE', 'Veracruz'), ('YU', 'Yucatan'), ('ZA', 'Zacatecas')], max_length=40, verbose_name='Estado')),
                ('calificacion', models.IntegerField(default=5, verbose_name='Calificación')),
                ('viajes_realizados', models.IntegerField(default=0, verbose_name='Viajes realizados')),
                ('licencia_conducir', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Número de licencia de conducir')),
                ('fecha_vencimiento_licencia', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de vencimiento de la licencia de manejo')),
                ('licencia_conducir_foto', models.ImageField(blank=True, null=True, upload_to='licencias_transportistas', verbose_name='Foto de licencia de conducir')),
                ('licencia_conducir_verificador_foto', models.ImageField(blank=True, null=True, upload_to='verificaciones', verbose_name='Foto de licencia de conducir de verificador')),
                ('licencia_mp', models.BooleanField(default=False, verbose_name='Permiso de transportación de material peligroso')),
                ('licencia_conducir_mp_foto', models.ImageField(blank=True, null=True, upload_to='licencias_transportistas', verbose_name='Foto de permiso para conducir material peligroso')),
                ('licencia_conducir_mp_verificador_foto', models.ImageField(blank=True, null=True, upload_to='verificaciones', verbose_name='Foto de permiso para conducir material peligroso de verificador')),
                ('notificacion_administrador', models.TextField(blank=True, null=True, verbose_name='Notificaciones para el transportista')),
                ('es_validado', models.BooleanField(default=False)),
                ('es_verificado', models.BooleanField(default=False)),
                ('es_activo', models.BooleanField(default=False)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Transportista',
                'verbose_name_plural': 'Transportistas',
            },
        ),
        migrations.CreateModel(
            name='Encierro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de encierro')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('external_number', models.CharField(max_length=10, verbose_name='Número exterior')),
                ('internal_number', models.CharField(blank=True, max_length=10, verbose_name='Número interior')),
                ('colonia', models.CharField(max_length=100, verbose_name='Colonia')),
                ('municipio', models.CharField(max_length=100, verbose_name='Municipio o alcaldía')),
                ('cp', models.CharField(max_length=5, verbose_name='Código postal')),
                ('estado', models.CharField(choices=[('AG', 'Aguascalientes'), ('BC', 'Baja California'), ('BS', 'Baja California Sur'), ('CM', 'Campeche'), ('CS', 'Chiapas'), ('CH', 'Chihuahua'), ('CO', 'Coahuila'), ('CL', 'Colima'), ('DF', 'Ciudad de Mexico'), ('DG', 'Durango'), ('GT', 'Guanajuato'), ('GR', 'Guerrero'), ('HG', 'Hidalgo'), ('JA', 'Jalisco'), ('MX', 'Mexico'), ('MI', 'Michoacan'), ('MO', 'Morelos'), ('NA', 'Nayarit'), ('NL', 'Nuevo Leon'), ('OA', 'Oaxaca'), ('PU', 'Puebla'), ('QT', 'Queretaro'), ('QR', 'Quintana Roo'), ('SL', 'San Luis Potosi'), ('SI', 'Sinaloa'), ('SO', 'Sonora'), ('TB', 'Tabasco'), ('TM', 'Tamaulipas'), ('TL', 'Tlaxcala'), ('VE', 'Veracruz'), ('YU', 'Yucatan'), ('ZA', 'Zacatecas')], max_length=40, verbose_name='Estado')),
                ('verificador_foto_encierro', models.ImageField(blank=True, null=True, upload_to='verificaciones', verbose_name='Foto de encierro de verificador')),
                ('verificador_direccion', models.CharField(blank=True, max_length=200, verbose_name='Dirección del domicilio fiscal')),
                ('es_validado', models.BooleanField(default=False)),
                ('es_verificado', models.BooleanField(default=False)),
                ('es_activo', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Encierro',
                'verbose_name_plural': 'Encierros',
            },
        ),
        migrations.CreateModel(
            name='Unidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50, verbose_name='Marca')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo')),
                ('año', models.IntegerField(choices=[(1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2024, verbose_name='Año')),
                ('tipo_caja', models.CharField(max_length=50, verbose_name='Tipo de caja')),
                ('capacidad_carga', models.FloatField(verbose_name='Capacidad de carga (toneladas)')),
                ('placa', models.CharField(max_length=15, unique=True, verbose_name='Placa')),
                ('tarjeta_circulacion', models.CharField(max_length=50, unique=True, verbose_name='Tarjeta de circulación')),
                ('tarjeta_circulacion_foto', models.ImageField(blank=True, null=True, upload_to='tarjetas_circulacion', verbose_name='Foto de tarjeta de circulación')),
                ('tarjeta_circulacion_verificador_foto', models.ImageField(blank=True, null=True, upload_to='verificaciones', verbose_name='Foto de tarjeta de circulación del verificador')),
                ('foto1', models.ImageField(blank=True, null=True, upload_to='unidades_pics', verbose_name='Foto 1 de unidad')),
                ('foto2', models.ImageField(blank=True, null=True, upload_to='unidades_pics', verbose_name='Foto 2 de unidad')),
                ('verificador_foto_unidad', models.ImageField(blank=True, null=True, upload_to='verificaciones', verbose_name='Foto de unidad del verificador')),
                ('es_verificado', models.BooleanField(default=False, verbose_name='Unidad verificada')),
                ('encierro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.encierro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
            },
        ),
        migrations.AddConstraint(
            model_name='unidades',
            constraint=models.UniqueConstraint(fields=('marca', 'modelo', 'año', 'user'), name='unique_unidad_user'),
        ),
    ]
