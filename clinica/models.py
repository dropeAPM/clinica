from django.db import models
from django.core.exceptions import ValidationError

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='especialidades/', blank=True, null=True)
    contacto = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='medicos')
    horario_inicio = models.TimeField(default='09:00')
    horario_fin = models.TimeField(default='17:00')
    max_atenciones_diarias = models.IntegerField(default=5)
    valor_consulta = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad.nombre}"

    def tiene_max_reservas(self, fecha):
        """
        Verifica si el médico ya tiene el máximo de reservas en una fecha específica.
        """
        return Reserva.objects.filter(medico=self, fecha=fecha).count() >= self.max_atenciones_diarias


class Reserva(models.Model):
    paciente = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    email = models.EmailField()  # Campo obligatorio
    telefono = models.CharField(max_length=12)  # Campo obligatorio
    codigo_descuento = models.CharField(max_length=5, blank=True, null=True)
    monto_pagado = models.DecimalField(max_digits=7, decimal_places=2)

    def calcular_descuento(self):
        if self.codigo_descuento and sum(int(digit) for digit in self.codigo_descuento) == 25:
            return self.monto_pagado * 0.75  # 25% de descuento
        return self.monto_pagado

    def __str__(self):
        return f"Reserva de {self.paciente} con {self.medico.nombre} el {self.fecha} a las {self.hora}"

    def clean(self):
        """
        Validación adicional: Verifica si el médico ya tiene una reserva en el mismo horario y si no ha alcanzado el máximo de reservas en el día.
        """
        if self.medico.tiene_max_reservas(self.fecha):
            raise ValidationError("El médico ya tiene el máximo de reservas para este día.")

        if Reserva.objects.filter(medico=self.medico, fecha=self.fecha, hora=self.hora).exclude(id=self.id).exists():
            raise ValidationError("El médico ya tiene una reserva en este horario.")

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para ejecutar la validación antes de guardar.
        """
        self.full_clean()  # Ejecuta clean() antes de guardar
        super().save(*args, **kwargs)
