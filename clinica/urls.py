from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reservar/', views.crear_reserva, name='crear_reserva'),
    path('ticket/<int:reserva_id>/', views.ver_ticket, name='ver_ticket'),
    path('get_medico_valor/', views.get_medico_valor, name='get_medico_valor'),
]
