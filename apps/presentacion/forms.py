from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Presentacion


class PresentacionForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre de la presentacion', 'class': 'form-control'})
            self.fields['abreviatura'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una Abreviatura', 'class': 'form-control'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una Descripcion', 'class': 'form-control'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Presentacion
        fields = ['nombre',
                  'abreviatura',
                  'descripcion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'abreviatura': 'Abreviatura',
            'descripcion': 'Descripcion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'abreviatura': forms.TextInput(),
            'descripcion': forms.TextInput()
        }
