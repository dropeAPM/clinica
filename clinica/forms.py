from django import forms
from .models import Reserva, Medico

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['paciente', 'medico', 'fecha', 'hora', 'codigo_descuento']

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una fecha',
                'type': 'text',
            }),
            'hora': forms.TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una hora',
                'type': 'text',
            }),
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'codigo_descuento': forms.TextInput(attrs={'class': 'form-control'}),
        }
