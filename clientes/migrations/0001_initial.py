# Generated by Django 5.0.3 on 2024-05-25 06:07

import django.db.models.deletion
import shared.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('foto_perfil', models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Foto de perfil')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre o Razon social(empresas)')),
                ('ape_pat', models.CharField(blank=True, max_length=100, verbose_name='Apellido paterno')),
                ('ape_mat', models.CharField(blank=True, max_length=100, verbose_name='Apellido materno')),
                ('telefono', models.CharField(max_length=11, validators=[shared.validators.phone_validator], verbose_name='Numero teléfonico a 10 digitos')),
                ('calle', models.CharField(max_length=100, verbose_name='Calle')),
                ('num_ext', models.CharField(max_length=100, verbose_name='Numero exterior')),
                ('num_int', models.CharField(blank=True, max_length=100, verbose_name='Numero interior')),
                ('colonia', models.CharField(max_length=100, verbose_name='Colonia')),
                ('municipio', models.CharField(max_length=100, verbose_name='Municipio o alcadía')),
                ('cp', models.CharField(max_length=6, validators=[shared.validators.cp_validator], verbose_name='Código postal')),
                ('estado', models.CharField(choices=[('Aguascalientes', 'Aguascalientes'), ('Baja California', 'Baja California'), ('Baja California Sur', 'Baja California Sur'), ('Campeche', 'Campeche'), ('Coahuila de Zaragoza', 'Coahuila de Zaragoza'), ('Colima', 'Colima'), ('Chiapas', 'Chiapas'), ('Chihuahua', 'Chihuahua'), ('CDMX', 'CDMX'), ('Durango', 'Durango'), ('Guanajuato', 'Guanajuato'), ('Guerrero', 'Guerrero'), ('Hidalgo', 'Hidalgo'), ('Jalisco', 'Jalisco'), ('México', 'México'), ('Michoacán de Ocampo', 'Michoacán de Ocampo'), ('Morelos', 'Morelos'), ('Nayarit', 'Nayarit'), ('Nuevo León', 'Nuevo León'), ('Oaxaca', 'Oaxaca'), ('Puebla', 'Puebla'), ('Querétaro', 'Querétaro'), ('Quintana Roo', 'Quintana Roo'), ('San Luis Potosí', 'San Luis Potosí'), ('Sinaloa', 'Sinaloa'), ('Sonora', 'Sonora'), ('Tabasco', 'Tabasco'), ('Tamaulipas', 'Tamaulipas'), ('Tlaxcala', 'Tlaxcala'), ('Veracruz de Ignacio de la Llave', 'Veracruz de Ignacio de la Llave'), ('Yucatán', 'Yucatán'), ('Zacatecas', 'Zacatecas')], max_length=40, verbose_name='Estado')),
                ('conektaId', models.CharField(blank=True, max_length=30, verbose_name='Conekta ID')),
                ('es_validado', models.BooleanField(default=False)),
                ('file_import', models.FileField(default='default.csv', max_length=254, upload_to='csvImports')),
                ('direccion_google', models.CharField(blank=True, max_length=200, null=True)),
                ('creado_at', models.DateTimeField(auto_now_add=True)),
                ('modificado_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
