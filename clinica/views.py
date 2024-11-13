from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Especialidad, Medico, Reserva
from .forms import ReservaForm
from django.contrib import messages
from django.db.models import Count

def home(request):
    especialidades = Especialidad.objects.all().prefetch_related('medicos')
    return render(request, 'clinica/home.html', {'especialidades': especialidades})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reservas_del_dia = Reserva.objects.filter(medico=reserva.medico, fecha=reserva.fecha)

            if reservas_del_dia.filter(hora=reserva.hora).exists():
                messages.error(request, "La hora seleccionada ya está reservada. Intente con otra.")
                return redirect('crear_reserva')

            reserva.monto_pagado = reserva.medico.valor_consulta
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

    return render(request, 'clinica/reserva.html', {
        'form': form,
        'fechas_bloqueadas': fechas_bloqueadas,
    })

def ver_ticket(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'clinica/ticket.html', {'reserva': reserva})

def get_medico_valor(request):
    medico_id = request.GET.get('medico_id')
    medico = get_object_or_404(Medico, id=medico_id)
    return JsonResponse({'valor_consulta': float(medico.valor_consulta)})
