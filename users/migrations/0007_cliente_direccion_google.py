# Generated by Django 5.0.3 on 2024-04-29 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_cliente_estado_alter_datosfiscales_estado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='direccion_google',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
