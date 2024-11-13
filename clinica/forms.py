from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    HORA_CHOICES = [
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
    ]

    hora = forms.ChoiceField(choices=HORA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Reserva
        fields = ['paciente', 'medico', 'fecha', 'hora', 'codigo_descuento']

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una fecha',
                'type': 'text',
            }),
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'codigo_descuento': forms.TextInput(attrs={'class': 'form-control'}),
        }

