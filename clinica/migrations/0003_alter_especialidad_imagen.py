# Generated by Django 5.1.1 on 2024-11-12 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_alter_medico_especialidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialidad',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='especialidades/'),
        ),
    ]
