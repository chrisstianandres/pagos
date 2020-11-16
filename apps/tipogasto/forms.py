from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Tipo_gasto


class TipogastoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del Servicio', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Tipo_gasto
        fields = ['nombre'
                  ]
        labels = {
            'nombre': 'Nombre'
        }
        widgets = {
            'nombre': forms.TextInput()
        }
