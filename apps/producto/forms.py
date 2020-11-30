from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Producto


class ProductoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del producto', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion del producto', 'class': 'form-control form-rounded'})
            self.fields['categoria'].widget.attrs = {
                'class': 'form-control select2'}
            self.fields['presentacion'].widget.attrs = {
                'class': 'form-control select2'}
            self.fields['pvp'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm'}

        # habilitar, desabilitar, y mas

    class Meta:
        model = Producto
        fields = ['nombre',
                  'descripcion',
                  'categoria',
                  'presentacion',
                  'pvp',
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion',
            'categoria': 'Categoria',
            'presentacion': 'Presentacion',
            'pvp': 'P.V.P.',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'pvp': forms.TextInput(),
            'decripcion': forms.Textarea(attrs={'col': '3', 'row': '2'})
        }
