from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from .models import Especialidad, Medico, Reserva
from .forms import ReservaForm

def home(request):
    especialidades = Especialidad.objects.all().prefetch_related('medicos')
    return render(request, 'clinica/home.html', {'especialidades': especialidades})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            # Validación para verificar si ya existe una reserva a la misma hora
            reservas_del_dia = Reserva.objects.filter(medico=reserva.medico, fecha=reserva.fecha)
            
            if reservas_del_dia.count() >= reserva.medico.max_atenciones_diarias:
                messages.error(request, "El médico ya tiene el máximo de reservas para este día.")
                return redirect('crear_reserva')
            
            if reservas_del_dia.filter(hora=reserva.hora).exists():
                messages.error(request, "El médico ya tiene una reserva a esta hora.")
                return redirect('crear_reserva')

            reserva.monto_pagado = reserva.medico.valor_consulta  # Ajuste para agregar monto pagado
            reserva.save()

            return redirect('ver_ticket', reserva_id=reserva.id)
    else:
        form = ReservaForm()

    fechas_bloqueadas = list(
        Reserva.objects.values('fecha')
        .annotate(reservas_count=Count('id'))
        .filter(reservas_count__gte=5)
        .values_list('fecha', flat=True)
    )
    fechas_bloqueadas = [fecha.strftime('%Y-%m-%d') for fecha in fechas_bloqueadas]

    horas_ocupadas = {}
    for reserva in Reserva.objects.all():
        fecha_str = reserva.fecha.strftime('%Y-%m-%d')
        if fecha_str not in horas_ocupadas:
            horas_ocupadas[fecha_str] = []
        horas_ocupadas[fecha_str].append(reserva.hora.strftime('%H:%M'))

    return render(request, 'clinica/reserva.html', {
        'form': form,
        'fechas_bloqueadas': fechas_bloqueadas,
        'horas_ocupadas': horas_ocupadas,
    })

def ver_ticket(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'clinica/ticket.html', {'reserva': reserva})

def get_medico_valor(request):
    medico_id = request.GET.get('medico_id')
    medico = get_object_or_404(Medico, id=medico_id)
    return JsonResponse({'valor_consulta': float(medico.valor_consulta)})
