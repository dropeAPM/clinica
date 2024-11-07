from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Especialidad, Medico, Reserva
from .forms import ReservaForm
from django.contrib import messages
from datetime import time
from django.core.files import File
from pathlib import Path

def home(request):
    # Verificar si existen especialidades en la base de datos
    if not Especialidad.objects.exists():
        default_image_path = Path('static/especialidades/default.jpg')

        cardiologia = Especialidad.objects.create(
            nombre="Cardiología",
            descripcion="Especialidad médica que se ocupa de las enfermedades del corazón.",
            contacto="cardiologia@clinicavida.com",
            ubicacion="Piso 2, Clínica Salud y Vida"
        )
        cardiologia.imagen.save('default.jpg', File(open(default_image_path, 'rb')))

        dermatologia = Especialidad.objects.create(
            nombre="Dermatología",
            descripcion="Especialidad médica que se ocupa del cuidado de la piel.",
            contacto="dermatologia@clinicavida.com",
            ubicacion="Piso 3, Clínica Salud y Vida"
        )
        dermatologia.imagen.save('default.jpg', File(open(default_image_path, 'rb')))
        
        Medico.objects.create(
            nombre="Dr. Juan Pérez",
            especialidad=cardiologia,
            horario_inicio="09:00",
            horario_fin="17:00",
            max_atenciones_diarias=5,
            valor_consulta=15000
        )
        Medico.objects.create(
            nombre="Dra. María González",
            especialidad=cardiologia,
            horario_inicio="09:00",
            horario_fin="17:00",
            max_atenciones_diarias=5,
            valor_consulta=18000
        )
        Medico.objects.create(
            nombre="Dr. Luis Ramírez",
            especialidad=dermatologia,
            horario_inicio="09:00",
            horario_fin="17:00",
            max_atenciones_diarias=5,
            valor_consulta=12000
        )

    especialidades = Especialidad.objects.all().prefetch_related('medicos')
    return render(request, 'clinica/home.html', {'especialidades': especialidades})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            reservas_existentes = Reserva.objects.filter(
                medico=reserva.medico,
                fecha=reserva.fecha
            )
            
            if reservas_existentes.count() >= reserva.medico.max_atenciones_diarias:
                messages.error(request, "El médico ya tiene el máximo de reservas para este día.")
                return redirect('crear_reserva')
            
            hora_inicio = time(9, 0)
            hora_fin = time(17, 0)

            if not (hora_inicio <= reserva.hora <= hora_fin):
                messages.error(request, "La hora debe estar entre las 9:00 y las 17:00.")
                return redirect('crear_reserva')

            reserva.monto_pagado = reserva.medico.valor_consulta
            reserva.monto_pagado = reserva.calcular_descuento()
            reserva.save()

            return redirect('ticket', reserva_id=reserva.id)
    else:
        form = ReservaForm()
    
    return render(request, 'clinica/reserva.html', {'form': form})

def ticket(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'clinica/ticket.html', {'reserva': reserva})

def get_medico_valor(request):
    medico_id = request.GET.get('medico_id')
    medico = get_object_or_404(Medico, id=medico_id)
    return JsonResponse({'valor_consulta': float(medico.valor_consulta)})
