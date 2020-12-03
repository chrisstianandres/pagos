from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput, Textarea

from .models import SitioWeb


class SitiowebForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['titulo'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el titulo del sitio', 'class': 'form-control form-rounded'})
            self.fields['mision'].widget = Textarea(
                attrs={'placeholder': 'Ingrese la mision de la empresa', 'class': 'form-control form-rounded'})
            self.fields['vision'].widget = Textarea(
                attrs={'placeholder': 'Ingrese la vision de la empresa', 'class': 'form-control form-rounded'})
            self.fields['mapa'].widget = Textarea(
                attrs={'placeholder': 'Copia y Pega un mapa de google', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = SitioWeb
        fields = ['titulo', 'mision', 'vision', 'mapa'
                  ]
        labels = {
            'titulo': 'Titulo', 'mision': 'Mision', 'vision': 'Vision', 'mapa': 'Mapa'
        }
        widgets = {
            'titulo': forms.TextInput(),
            'mision': forms.Textarea(),
            'vision': forms.TextInput(),
            'mapa': forms.Textarea()
        }
