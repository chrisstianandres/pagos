from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Maquina, Tipo_maquina


class TipomaquinaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre de la maquina', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Tipo_maquina
        fields = ['nombre', 'descripcion',
                  ]
        labels = {
            'nombre': 'Nombre', 'descripcion': 'Descripcion',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput()
        }


class MaquinaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['tipo'].widget.attrs = {
                'class': 'form-control select2'

            }
            self.fields['serie'].widget.attrs = {
                'class': 'form-control'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Maquina
        fields = ['tipo', 'serie']
        labels = {
            'tipo': 'Tipo de Maquina', 'serie': 'Serie',
        }
        widgets = {
            'serie': forms.TextInput()
        }