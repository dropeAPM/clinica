# Generated by Django 5.1.1 on 2024-11-13 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0004_reserva_email_reserva_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
