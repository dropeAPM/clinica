# Generated by Django 5.1.1 on 2024-11-13 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0009_alter_reserva_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='monto_pagado',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
