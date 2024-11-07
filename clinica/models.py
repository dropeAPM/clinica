from django.db import models

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

class Reserva(models.Model):
    paciente = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    codigo_descuento = models.CharField(max_length=5, blank=True, null=True)
    monto_pagado = models.DecimalField(max_digits=7, decimal_places=2)

    def calcular_descuento(self):
        if self.codigo_descuento and sum(int(digit) for digit in self.codigo_descuento) == 25:
            return self.monto_pagado * 0.75  # 25% de descuento
        return self.monto_pagado

    def __str__(self):
        return f"Reserva de {self.paciente} con {self.medico.nombre} el {self.fecha} a las {self.hora}"

