from django import forms
from datetime import *

from django.contrib.auth.models import Group
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from apps.producto.models import Producto
from apps.producto_base.models import Producto_base


class Producto_baseForm(forms.ModelForm):
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

    class Meta:
        model = Producto_base
        fields = ['nombre',
                  'descripcion',
                  'categoria',
                  'presentacion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion',
            'categoria': 'Categoria',
            'presentacion': 'Presentacion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'decripcion': forms.Textarea(attrs={'col': '3', 'row': '2'})
        }


class ProductoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['pvp'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm',
                'value': 1}

    class Meta:
        model = Producto
        fields = ['pvp']
        labels = {'pvp': 'P.V.P.'}
        widgets = {'pvp': forms.TextInput()}


class GroupForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['name'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm'}

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {'name': 'Nombre', 'permissions': 'Permisos'}
        widgets = {'name': forms.TextInput(),
                   'permissions': forms.SelectMultiple(attrs={
                       'class': 'form-control c',
                       'style': 'width: 100%',
                       'multiple': 'multiple'
                   })}
