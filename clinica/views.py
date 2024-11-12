from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Especialidad, Medico, Reserva
from .forms import ReservaForm
from django.contrib import messages
from datetime import time
from django.db.models import Count

def home(request):
    # Verificar si existen especialidades en la base de datos y crearlas si no existen
    # (código de creación de datos omitido para brevedad)

    especialidades = Especialidad.objects.all().prefetch_related('medicos')
    return render(request, 'clinica/home.html', {'especialidades': especialidades})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            # Verificar que no haya más de 5 reservas para el médico en esa fecha
            reservas_del_dia = Reserva.objects.filter(
                medico=reserva.medico,
                fecha=reserva.fecha
            )
            
            if reservas_del_dia.count() >= reserva.medico.max_atenciones_diarias:
                messages.error(request, "El médico ya tiene el máximo de reservas para este día.")
                return redirect('crear_reserva')

            # Verificar que la hora no esté ocupada por otra reserva del mismo médico
            if reservas_del_dia.filter(hora=reserva.hora).exists():
                messages.error(request, "El médico ya tiene una reserva a esta hora.")
                return redirect('crear_reserva')

            # Guardar la reserva si pasa todas las validaciones
            reserva.monto_pagado = reserva.medico.valor_consulta
            reserva.monto_pagado = reserva.calcular_descuento()
            reserva.save()

            return redirect('ticket', reserva_id=reserva.id)
    else:
        form = ReservaForm()

        # Obtener las fechas bloqueadas para cada médico (fechas con 5 o más reservas)
        fechas_bloqueadas = Reserva.objects.values('fecha').annotate(
            reservas_count=Count('id')
        ).filter(
            reservas_count__gte=5
        ).values_list('fecha', flat=True)

    return render(request, 'clinica/reserva.html', {
        'form': form,
        'fechas_bloqueadas': list(fechas_bloqueadas)
    })

def ticket(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'clinica/ticket.html', {'reserva': reserva})

def get_medico_valor(request):
    medico_id = request.GET.get('medico_id')
    medico = get_object_or_404(Medico, id=medico_id)
    return JsonResponse({'valor_consulta': float(medico.valor_consulta)})
