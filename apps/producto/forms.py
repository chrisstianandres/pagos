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
                attrs={'placeholder': 'Ingrese el nombre del producto', 'class': 'form-control form-rounded',
                       'id': 'id_nombre_producto'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion del producto', 'class': 'form-control form-rounded'})
            self.fields['categoria'].widget.attrs = {
                'class': 'form-control select2',
                'id': 'id_despcripcion_producto', 'style': 'width: 95%'}
            self.fields['color'].widget.attrs = {
                'class': 'form-control select2', 'style': 'width: 95%'}

    class Meta:
        model = Producto_base
        fields = ['nombre',
                  'descripcion',
                  'categoria',
                  'color'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion',
            'categoria': 'Categoria',
            'color': 'Color'
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
            # self.fields[field].widget.attrs.update({
            #     'class': 'form-control'
            # })
            self.fields['pvp'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm',
                'value': 1}
            self.fields['producto_base'].widget.attrs = {
                'class': 'form-control select2'}
            # self.fields['producto_base'].queryset = Producto_base.objects.none()
            self.fields['pvp_alq'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm',
                'value': 1}
            self.fields['pvp_confec'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm',
                'value': 1}
            self.fields['presentacion'].widget.attrs = {
                'class': 'form-control select2',
                'id': 'id_presentacion_producto'}
            self.fields['talla'].widget.attrs = {
                'class': 'form-control select2'}

    class Meta:
        model = Producto
        fields = ['producto_base', 'pvp', 'pvp_alq', 'pvp_confec', 'imagen', 'presentacion', 'talla']
        labels = {'producto_base': 'Producto', 'pvp': 'P.V.P.', 'pvp_alq': 'Precio Alquiler.',  'talla': 'Talla',
                  'pvp_confec': 'Precio Confeccion.', 'imagen': 'Imagen',  'presentacion': 'Presentacion'}
        widgets = {'pvp': forms.TextInput(), 'pvp_alq': forms.TextInput(), 'pvp_confec': forms.TextInput()}


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
